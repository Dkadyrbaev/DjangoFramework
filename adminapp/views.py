from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from adminapp.forms import ProductEditForm, ProductForm, ShopUserAdminEditForm, ProductCategoryForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator


class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self):
        context = super(UserListView, self).get_context_data()
        title = 'админка/пользователи'
        context.update({'title': title})

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserCreateView, self).get_context_data()
        title = 'пользователи/создание'
        context.update({'title': title})

        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self):
        context = super(UserUpdateView, self).get_context_data()
        title = 'админка/редактирование'
        context.update({'title': title})

        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data()
        title = 'админка/категории'
        context.update({'title': title})

        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self):
        context = super(ProductCategoryCreateView, self).get_context_data()
        title = 'категории/создание'
        context.update({'title': title})

        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    # fields = '__all__'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self):
        context = super(ProductCategoryUpdateView, self).get_context_data()
        title = 'категории/редактирование'
        context.update({'title': title})

        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductForm

    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        return reverse_lazy('adminapp:products', args=[product.category.pk])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            pk = self.kwargs.get('pk')
            category_item = get_object_or_404(ProductCategory, pk=pk)
            context_data['category'] = category_item
            title = 'продукты/создание'
            context_data['title'] = title
        return context_data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    # fields = '__all__'
    form_class = ProductForm

    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_pk)
        return reverse_lazy('adminapp:products', args=[product.category.pk])


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        return reverse_lazy('adminapp:products', args=[product.category.pk])

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
