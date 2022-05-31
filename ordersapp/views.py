from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderItemForm, OrderForm
from ordersapp.models import Order, OrderItem
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


def is_ajax(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


class TitleContextMixin:
    def get_title(self):
        return getattr(self, 'title', '')

    def get_context_data(self, **kwargs):
        context = super(TitleContextMixin, self).get_context_data(**kwargs)
        context.update(
            title=self.get_title()
        )
        return context


class OrderListView(TitleContextMixin, ListView):
    model = Order
    title = 'Список заказов'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)

    # @method_decorator(login_required())
    # def dispatch(self, *args, **kwargs):
    #     return super(ListView, self).dispatch(*args, **kwargs)


class OrderCreateView(TitleContextMixin, CreateView):
    model = Order
    title = 'Создание заказа'
    fields = []
    success_url = reverse_lazy('ordersapp:main')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm, extra=len(basket_items)
                )
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items[num].delete()
            else:
                formset = OrderFormSet()
        context.update(
            orderitems=formset
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # basket_items = Basket.objects.filter(user=self.request.user)
            # basket_items.delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(TitleContextMixin, UpdateView):
    model = Order
    title = 'Изменение заказа'
    fields = []
    success_url = reverse_lazy('ordersapp:main')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost == 0:
            self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(TitleContextMixin, DeleteView):
    model = Order
    title = 'Удаление заказа'
    success_url = reverse_lazy('ordersapp:main')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


class OrderDetailView(TitleContextMixin, DetailView):
    model = Order
    title = 'заказ/просмотр'

    # def get_context_data(self, **kwargs):
    #     context = super(OrderDetailView, self).get_context_data(**kwargs)
    #     context['title'] = 'заказ/просмотр'
    #     return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:main'))


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is 'quantity' or 'product':
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    if is_ajax(request):
        product = Product.objects.filter(pk=int(pk)).first()
        if product:
            return JsonResponse({'price': product.price})
        else:
            return JsonResponse({'price': 0})
