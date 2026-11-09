from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError

from loja.forms import ProductForm, SaleRowForm
from loja.models import Product
from loja.services import register_sale
from uuid import uuid4
from .base import ShopTestCase


class ProductTests(ShopTestCase):
    def data(self, **changes):
        return {'name': 'Produto fictício', 'price': '8.50', 'stock': '3', 'unit': 'UN', 'active': 'on', **changes}

    def test_product_valid(self):
        form = ProductForm(self.data())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(str(form.save()), 'Produto fictício')

    def test_product_invalid_fields(self):
        for change in [{'name': ''}, {'name': '<script>alert(1)</script>'}, {'price': '-1'},
                       {'price': '0'}, {'stock': '-1'}, {'stock': '1.5'}, {'unit': 'XX'},
                       {'price': 'NaN'}, {'stock': 'Infinity'}, {'name': 'x' * 121}]:
            with self.subTest(change=change):
                self.assertFalse(ProductForm(self.data(**change)).is_valid())

    def test_weight_fraction_allowed(self):
        self.assertTrue(ProductForm(self.data(stock='1.250', unit='KG')).is_valid())

    def test_model_validation(self):
        self.unit.stock = Decimal('1.5')
        with self.assertRaises(ValidationError):
            self.unit.full_clean()

    def test_database_rejects_negative_stock(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.filter(pk=self.product.pk).update(stock=-1)

    def test_product_referenced_by_sale_cannot_be_deleted(self):
        register_sale(user=self.owner, operation_key=uuid4(), rows=[{'product_id': self.product.pk, 'quantity': 1}])
        with self.assertRaises(ProtectedError):
            self.product.delete()

    def test_form_choice_excludes_inactive(self):
        self.product.active = False
        self.product.save()
        form = SaleRowForm({'product': self.product.pk, 'quantity': 1})
        self.assertFalse(form.is_valid())

    def test_decimal_comma_and_label(self):
        form = SaleRowForm({'product': self.product.pk, 'quantity': '0,500'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['quantity'], Decimal('.500'))
        self.assertIn('Disponível', form.fields['product'].label_from_instance(self.product))
