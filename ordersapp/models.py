from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 1
    SEND_TO_PROCEED = 2
    PAID = 3
    PROCEED = 4
    READY = 5
    CANCEL = 6

    ORDER_STATUSES = (
        (FORMING, 'Формируется'),
        (SEND_TO_PROCEED, 'В обработке'),
        (PAID, 'Оплачен'),
        (PROCEED, 'Собирается'),
        (READY, 'Готов'),
        (CANCEL, 'Отменён'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        verbose_name='время создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        verbose_name='время изменения',
        auto_now=True
    )
    status = models.PositiveIntegerField(
        choices=ORDER_STATUSES,
        verbose_name='Статус',
        default=FORMING
    )
    is_active = models.BooleanField(
        verbose_name='Активен ли',
        default=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ {self.pk}'

    # @property
    # def get_total_cost(self):
    #     items = self.items.select_related()
    #     return sum(list(map(lambda x: x.cost, items)))
    #
    # @property
    # def get_total_quantity(self):
    #     items = self.items.select_related()
    #     return sum(list(map(lambda x: x.quantity, items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items))),
        }

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()


class OrderItemQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='orderitems',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity
