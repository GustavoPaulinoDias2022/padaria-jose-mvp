from getpass import getpass

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = 'Cria conta autorizada, sem senha padrão e sem privilégios de superusuário.'

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        username = options['username']
        user = get_user_model()(username=username)
        password = getpass('Senha (mínimo 15 caracteres): ')
        if password != getpass('Repita a senha: '):
            raise CommandError('As senhas não coincidem.')
        try:
            user.full_clean(exclude=['password'])
            validate_password(password, user)
        except ValidationError as exc:
            raise CommandError('; '.join(exc.messages)) from None
        with transaction.atomic():
            user.set_password(password)
            user.save()
            user.user_permissions.add(Permission.objects.get(codename='operate_shop', content_type__app_label='loja'))
        self.stdout.write(self.style.SUCCESS('Conta criada com permissão de operação.'))
