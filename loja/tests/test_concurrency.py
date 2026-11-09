from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db import close_old_connections, connection
from django.test import TransactionTestCase

from loja.models import Product, Sale
from loja.services import SaleError, register_sale


@skipUnless(connection.vendor == 'postgresql', 'Concorrência exige PostgreSQL real; SQLite não comprova bloqueios de linha.')
class PostgreSQLConcurrencyTests(TransactionTestCase):
    def test_two_sales_cannot_oversell(self):
        user = get_user_model().objects.create_user(username='concorrencia_ficticia')
        user.user_permissions.add(Permission.objects.get(codename='operate_shop', content_type__app_label='loja'))
        product = Product.objects.create(name='Teste concorrente', price=2, stock=3, unit='UN')
        barrier = Barrier(2)

        def worker():
            close_old_connections()
            try:
                actor = get_user_model().objects.get(pk=user.pk)
                barrier.wait(timeout=15)
                try:
                    register_sale(user=actor, operation_key=uuid4(), rows=[{'product_id': product.pk, 'quantity': 2}])
                    return 'confirmed'
                except SaleError:
                    return 'rejected'
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: worker(), range(2)))
        self.assertCountEqual(results, ['confirmed', 'rejected'])
        product.refresh_from_db()
        self.assertEqual(product.stock, 1)
        self.assertEqual(Sale.objects.count(), 1)
