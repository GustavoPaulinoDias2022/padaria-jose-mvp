from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.db import DatabaseError

from loja.models import Product, Sale, SaleItem
from loja.services import SaleError, can_operate, preview_sale, register_sale
from .base import ShopTestCase


class SaleServiceTests(ShopTestCase):
    def sell(self, rows=None, key=None, user=None):
        return register_sale(user=user or self.owner, operation_key=key or uuid4(),
                             rows=rows if rows is not None else [{'product_id': self.product.pk, 'quantity': '0,500'}])

    def test_sale_updates_stock_and_records_snapshot(self):
        sale = self.sell()
        self.product.refresh_from_db()
        self.assertEqual(sale.total, Decimal('10.00'))
        self.assertEqual(self.product.stock, Decimal('4.500'))
        self.assertEqual(sale.user, self.owner)
        self.assertEqual(sale.items.get().product_name, self.product.name)

    def test_multiple_products_and_rounding(self):
        sale = self.sell([{'product_id': self.product.pk, 'quantity': '.501'}, {'product_id': self.unit.pk, 'quantity': 2}])
        self.assertEqual(sale.total, Decimal('27.02'))
        self.assertEqual(sale.items.count(), 2)
        self.product.price = Decimal('0.05')
        self.product.save()
        self.assertEqual(self.sell([{'product_id': self.product.pk, 'quantity': '.100'}]).total, Decimal('.01'))

    def test_duplicate_key_returns_same_sale(self):
        key = uuid4()
        first = self.sell(key=key)
        self.assertEqual(self.sell(key=key).pk, first.pk)
        self.assertEqual(Sale.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, Decimal('4.500'))

    def test_key_with_different_payload_rejected(self):
        key = uuid4()
        self.sell(key=key)
        with self.assertRaises(SaleError):
            self.sell([{'product_id': self.product.pk, 'quantity': 1}], key=key)

    def test_key_belongs_to_other_owner(self):
        key = uuid4()
        self.sell(key=key)
        self.other.user_permissions.set(self.owner.user_permissions.all())
        with self.assertRaises(SaleError):
            self.sell(key=key, user=self.other)

    def test_permissions(self):
        self.assertFalse(can_operate(AnonymousUser()))
        self.assertFalse(can_operate(self.other))
        for actor in [self.other, AnonymousUser()]:
            with self.subTest(actor=str(actor)), self.assertRaises(PermissionDenied):
                self.sell(user=actor)
        self.owner.is_active = False
        self.assertFalse(can_operate(self.owner))

    def test_invalid_uuid(self):
        with self.assertRaises(SaleError):
            self.sell(key='bad-key')

    def test_invalid_rows(self):
        cases = [[], {}, [None], [{}], [{'product_id': 'bad', 'quantity': 1}],
                 [{'product_id': -1, 'quantity': 1}], [{'product_id': 1, 'quantity': 'NaN'}],
                 [{'product_id': 1, 'quantity': 'Infinity'}], [{'product_id': 1, 'quantity': 'abc'}],
                 [{'product_id': 1, 'quantity': 0}], [{'product_id': 1, 'quantity': -1}],
                 [{'product_id': 1, 'quantity': '1000000000'}], [{'product_id': 1, 'quantity': '.0001'}],
                 [{'product_id': 1, 'quantity': 1}] * 21,
                 [{'product_id': self.product.pk, 'quantity': 1}] * 2]
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(SaleError):
                self.sell(rows)
        self.assertEqual(Sale.objects.count(), 0)

    def test_insufficient_inactive_missing_and_fractional(self):
        for rows in [[{'product_id': self.product.pk, 'quantity': 6}],
                     [{'product_id': 999999, 'quantity': 1}],
                     [{'product_id': self.unit.pk, 'quantity': '.5'}]]:
            with self.subTest(rows=rows), self.assertRaises(SaleError):
                self.sell(rows)
        self.product.active = False
        self.product.save()
        with self.assertRaises(SaleError):
            self.sell()
        self.assertFalse(Sale.objects.exists())

    def test_failure_rolls_back_sale_items_and_stock(self):
        with patch('loja.services.SaleItem.objects.create', side_effect=DatabaseError('test failure')):
            with self.assertRaises(DatabaseError):
                self.sell()
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, Decimal('5.000'))
        self.assertFalse(Sale.objects.exists())
        self.assertFalse(SaleItem.objects.exists())

    def test_changed_stock_rolls_back(self):
        with patch('django.db.models.query.QuerySet.update', return_value=0):
            with self.assertRaises(SaleError):
                self.sell()
        self.assertFalse(Sale.objects.exists())

    def test_total_bounds(self):
        self.product.price = Decimal('.01')
        self.product.save()
        with self.assertRaises(SaleError):
            self.sell([{'product_id': self.product.pk, 'quantity': '.001'}])
        self.product.price = Decimal('9999999999.99')
        self.product.save()
        with self.assertRaises(SaleError):
            self.sell([{'product_id': self.product.pk, 'quantity': 2}])

    def test_historical_values_survive_product_changes(self):
        sale = self.sell()
        self.product.name = 'Outro nome'
        self.product.price = Decimal('99')
        self.product.save()
        item = sale.items.get()
        self.assertEqual(item.unit_price, Decimal('20'))
        self.assertEqual(item.product_name, 'Pão francês fictício')

    def test_preview_does_not_write(self):
        result = preview_sale(user=self.owner, rows=[{'product_id': self.product.pk, 'quantity': '.5'}])
        self.assertEqual(result['total'], Decimal('10'))
        self.assertFalse(Sale.objects.exists())
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, Decimal('5'))

    def test_preview_errors(self):
        with self.assertRaises(PermissionDenied):
            preview_sale(user=self.other, rows=[])
        for pk, quantity in [(99999, 1), (self.unit.pk, '.5'), (self.product.pk, 6)]:
            with self.subTest(pk=pk, q=quantity), self.assertRaises(SaleError):
                preview_sale(user=self.owner, rows=[{'product_id': pk, 'quantity': quantity}])
        self.product.price = Decimal('.01')
        self.product.save()
        with self.assertRaises(SaleError):
            preview_sale(user=self.owner, rows=[{'product_id': self.product.pk, 'quantity': '.001'}])
