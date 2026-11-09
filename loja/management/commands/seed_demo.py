import os
from django.core.management.base import BaseCommand
from loja.models import Product


class Command(BaseCommand):
    help = 'Cria apenas produtos fictícios quando SEED_DEMO_DATA=1; não altera saldos existentes.'

    def handle(self, *args, **options):
        if os.environ.get('SEED_DEMO_DATA') != '1':
            self.stdout.write('Carga demonstrativa desativada.')
            return
        for name, price, stock, unit in [
            ('Pão francês — demonstração', '20.00', '5.000', 'KG'),
            ('Bolo de cenoura — demonstração', '18.00', '6.000', 'UN'),
            ('Pão de queijo — demonstração', '32.00', '3.500', 'KG'),
            ('Café em pacote — demonstração', '14.50', '12.000', 'UN'),
        ]:
            Product.objects.get_or_create(name=name, defaults={'price': price, 'stock': stock, 'unit': unit})
        self.stdout.write('Produtos fictícios preparados sem substituir registros existentes.')
