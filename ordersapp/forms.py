from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    # price = forms.CharField(
    #     label='цена',
    #     required=True,
    # )
    #
    # class Meta:
    #     model = OrderItem
    #     fields = '__all__'

    class Meta:
        model = OrderItem
        exclude = ()

    price = forms.CharField(
        label='цена',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['product'].queryset = Product.objects.filter(is_active=True, quantity__gte=1)
