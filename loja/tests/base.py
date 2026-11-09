from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from loja.models import Product

TEST_PASSWORD = 'uma-frase-ficticia-exclusiva-para-testes-2026!'


class ShopTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(username='operadora_teste', password=TEST_PASSWORD)
        cls.owner.user_permissions.add(Permission.objects.get(codename='operate_shop', content_type__app_label='loja'))
        cls.other = get_user_model().objects.create_user(username='sem_permissao', password=TEST_PASSWORD)
        cls.product = Product.objects.create(name='Pão francês fictício', price=Decimal('20.00'), stock=Decimal('5.000'), unit='KG')
        cls.unit = Product.objects.create(name='Bolo teste', price=Decimal('8.50'), stock=Decimal('3.000'), unit='UN')

    def login(self):
        self.client.force_login(self.owner, backend='django.contrib.auth.backends.ModelBackend')
