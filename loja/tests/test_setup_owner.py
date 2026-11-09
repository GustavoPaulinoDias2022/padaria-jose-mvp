from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError

from .base import ShopTestCase, TEST_PASSWORD


class OwnerCommandTests(ShopTestCase):
    def test_setup_owner(self):
        with patch('loja.management.commands.setup_owner.getpass', return_value=TEST_PASSWORD):
            call_command('setup_owner', 'nova_operadora', stdout=StringIO())
        user = get_user_model().objects.get(username='nova_operadora')
        self.assertTrue(user.has_perm('loja.operate_shop'))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password(TEST_PASSWORD))

    def test_password_mismatch(self):
        with patch('loja.management.commands.setup_owner.getpass', side_effect=['a', 'b']):
            with self.assertRaises(CommandError):
                call_command('setup_owner', 'nova', stdout=StringIO())

    def test_password_validation_and_duplicate_user(self):
        for username, password in [('nova', '123'), (self.owner.username, TEST_PASSWORD)]:
            with self.subTest(username=username), patch('loja.management.commands.setup_owner.getpass', return_value=password):
                with self.assertRaises(CommandError):
                    call_command('setup_owner', username, stdout=StringIO())
