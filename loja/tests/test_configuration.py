import os
import runpy
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase


class ConfigurationTests(SimpleTestCase):
    def settings(self, **environment):
        with patch.dict(os.environ, environment, clear=True):
            return runpy.run_path('config/settings.py')

    def test_production_requires_secret(self):
        with self.assertRaises(ImproperlyConfigured):
            self.settings(APP_ENV='production')

    def test_production_requires_postgresql(self):
        with self.assertRaises(ImproperlyConfigured):
            self.settings(APP_ENV='production', DJANGO_SECRET_KEY='test-only-' * 8)

    def test_wrong_database_scheme_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            self.settings(DATABASE_URL='mysql://localhost/test')

    def test_production_rejects_database_without_tls(self):
        with self.assertRaises(ImproperlyConfigured):
            self.settings(APP_ENV='production', DJANGO_SECRET_KEY='test-only-' * 8,
                          DATABASE_URL='postgresql://ci:ci@localhost/ci?sslmode=disable')

    def test_render_hostname_is_explicitly_allowed(self):
        result = self.settings(RENDER_EXTERNAL_HOSTNAME='padaria-exemplo.onrender.com')
        self.assertIn('padaria-exemplo.onrender.com', result['ALLOWED_HOSTS'])
        self.assertNotIn('*', result['ALLOWED_HOSTS'])

    def test_production_secure_flags_and_parsed_database(self):
        result = self.settings(APP_ENV='production', DJANGO_SECRET_KEY='test-only-' * 8,
                               DATABASE_URL='postgresql://ci_user:ci_password@localhost:5432/ci_db',
                               TRUST_HTTPS_PROXY='1', DJANGO_ALLOWED_HOSTS='padaria.invalid')
        self.assertFalse(result['DEBUG'])
        self.assertTrue(result['SESSION_COOKIE_SECURE'])
        self.assertTrue(result['CSRF_COOKIE_SECURE'])
        self.assertTrue(result['SECURE_SSL_REDIRECT'])
        self.assertEqual(result['DATABASES']['default']['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(result['DATABASES']['default']['OPTIONS']['sslmode'], 'require')
        self.assertEqual(result['SECURE_PROXY_SSL_HEADER'], ('HTTP_X_FORWARDED_PROTO', 'https'))

    def test_development_is_explicitly_distinct(self):
        result = self.settings(DATABASE_URL='postgresql://ci_user:p%40ss@localhost/ci_db?sslmode=disable')
        self.assertEqual(result['DATABASES']['default']['PASSWORD'], 'p@ss')
        self.assertEqual(result['DATABASES']['default']['PORT'], 5432)
        self.assertEqual(result['DATABASES']['default']['OPTIONS']['sslmode'], 'disable')
        self.assertNotIn('SECURE_PROXY_SSL_HEADER', result)
