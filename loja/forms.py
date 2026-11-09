from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory

from .models import Product


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Não foi possível entrar. Confira os dados e tente novamente.',
        'inactive': 'Não foi possível entrar. Confira os dados e tente novamente.',
    }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'unit', 'active']
        widgets = {'stock': forms.NumberInput(attrs={'step': '0.001', 'min': '0'}),
                   'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'})}


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, product):
        return f'{product.name} | R$ {product.price}/{product.unit} | Disponível: {product.stock} {product.unit}'


class SaleRowForm(forms.Form):
    product = ProductChoiceField(label='Produto', queryset=Product.objects.filter(active=True))
    quantity = forms.DecimalField(label='Quantidade', max_digits=12, decimal_places=3, min_value=0.001,
                                 localize=True, help_text='Use vírgula ou ponto; UN aceita somente inteiros.')


SaleFormSet = formset_factory(SaleRowForm, extra=0, max_num=20, validate_max=True,
                             min_num=1, validate_min=True, absolute_max=20)
