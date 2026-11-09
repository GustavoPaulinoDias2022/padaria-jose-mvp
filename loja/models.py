from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    class Unit(models.TextChoices):
        UN = 'UN', 'Unidade'
        KG = 'KG', 'Quilograma'

    name = models.CharField('Nome', max_length=120)
    price = models.DecimalField('Preço', max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.DecimalField('Estoque', max_digits=12, decimal_places=3, validators=[MinValueValidator(0)])
    unit = models.CharField('Unidade', max_length=2, choices=Unit.choices)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        ordering = ['name', 'pk']
        permissions = [('operate_shop', 'Operar produtos, vendas e estoque da padaria')]
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gt=0), name='product_positive_price'),
            models.CheckConstraint(condition=models.Q(stock__gte=0), name='product_nonnegative_stock'),
            models.CheckConstraint(condition=models.Q(unit__in=['UN', 'KG']), name='product_known_unit'),
        ]

    def clean(self):
        if '<' in self.name or '>' in self.name:
            raise ValidationError({'name': 'Use texto simples, sem marcação HTML.'})
        if self.unit == self.Unit.UN and self.stock is not None and self.stock != self.stock.to_integral_value():
            raise ValidationError({'stock': 'Produtos em UN exigem quantidade inteira.'})

    def __str__(self):
        return self.name


class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    operation_key = models.UUIDField(unique=True)
    fingerprint = models.CharField(max_length=64)

    class Meta:
        ordering = ['-created_at', '-pk']
        constraints = [models.CheckConstraint(condition=models.Q(total__gt=0), name='sale_positive_total')]


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=120)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=2, choices=Product.Unit.choices)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name='item_positive_quantity'),
            models.CheckConstraint(condition=models.Q(unit_price__gt=0), name='item_positive_price'),
            models.CheckConstraint(condition=models.Q(subtotal__gte=0), name='item_nonnegative_subtotal'),
            models.UniqueConstraint(fields=['sale', 'product'], name='one_product_per_sale'),
        ]
