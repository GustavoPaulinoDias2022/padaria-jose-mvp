"""Provisionamento inicial por segredos de ambiente, sem senha padrão."""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = 'Cria a primeira conta a partir de INITIAL_OWNER_USERNAME e INITIAL_OWNER_PASSWORD.'

    def handle(self, *args, **options):
        username = os.environ.get('INITIAL_OWNER_USERNAME', '')
        password = os.environ.get('INITIAL_OWNER_PASSWORD', '')
        if not username and not password:
            self.stdout.write('Provisionamento inicial não solicitado.')
            return
        if not username or not password:
            raise CommandError('Configure os dois segredos de provisionamento inicial.')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write('Conta existente preservada; senha não alterada.')
            return
        user = User(username=username)
        try:
            user.full_clean(exclude=['password'])
            validate_password(password, user)
        except ValidationError:
            raise CommandError('Credenciais iniciais inválidas; revise formato e política de senha.') from None
        with transaction.atomic():
            user.set_password(password)
            user.save()
            user.user_permissions.add(Permission.objects.get(codename='operate_shop', content_type__app_label='loja'))
        self.stdout.write('Conta inicial criada com permissão de operação.')
