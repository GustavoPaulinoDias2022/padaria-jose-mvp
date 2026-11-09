import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.db import DatabaseError

from loja.models import Product
from .base import ShopTestCase, TEST_PASSWORD


class DeploymentTests(ShopTestCase):
    def test_health_checks_database_without_details(self):
        self.assertEqual(self.client.get('/healthz/').json(), {'status': 'ok'})
        self.assertEqual(self.client.post('/healthz/').status_code, 405)
        with patch('loja.health.connection.cursor', side_effect=DatabaseError('secret-db-url')):
            response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})
        self.assertNotIn(b'secret-db-url', response.content)

    def bootstrap(self, **env):
        with patch.dict(os.environ, env, clear=True):
            call_command('bootstrap_owner', stdout=StringIO())

    def test_bootstrap_without_configuration_does_nothing(self):
        self.bootstrap()
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_partial_or_weak_credentials_fail_without_exposure(self):
        for env in [{'INITIAL_OWNER_USERNAME': 'nova'},
                    {'INITIAL_OWNER_USERNAME': 'nova', 'INITIAL_OWNER_PASSWORD': '123'}]:
            with self.subTest(env=env), self.assertRaises(CommandError):
                self.bootstrap(**env)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_bootstrap_grants_only_operation_and_never_resets(self):
        env = {'INITIAL_OWNER_USERNAME': 'implantacao_ficticia', 'INITIAL_OWNER_PASSWORD': TEST_PASSWORD}
        self.bootstrap(**env)
        user = get_user_model().objects.get(username=env['INITIAL_OWNER_USERNAME'])
        self.assertTrue(user.check_password(TEST_PASSWORD))
        self.assertTrue(user.has_perm('loja.operate_shop'))
        self.assertFalse(user.is_superuser)
        self.bootstrap(**{**env, 'INITIAL_OWNER_PASSWORD': TEST_PASSWORD + 'changed'})
        user.refresh_from_db()
        self.assertTrue(user.check_password(TEST_PASSWORD))

    def test_demo_seed_is_opt_in_and_preserves_stock(self):
        initial = Product.objects.count()
        with patch.dict(os.environ, {}, clear=True):
            call_command('seed_demo', stdout=StringIO())
        self.assertEqual(Product.objects.count(), initial)
        with patch.dict(os.environ, {'SEED_DEMO_DATA': '1'}, clear=True):
            call_command('seed_demo', stdout=StringIO())
            product = Product.objects.get(name='Pão francês — demonstração')
            product.stock = 1
            product.save()
            call_command('seed_demo', stdout=StringIO())
        product.refresh_from_db()
        self.assertEqual(product.stock, 1)
        self.assertEqual(Product.objects.count(), initial + 4)
