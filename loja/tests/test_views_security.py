import time
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from axes.models import AccessAttempt
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import DatabaseError
from django.test import Client, override_settings
from django.urls import reverse
from django.utils import timezone

from loja.models import Product, Sale
from .base import ShopTestCase, TEST_PASSWORD


class ViewSecurityTests(ShopTestCase):
    def sale_payload(self, **changes):
        return {'operation_key': str(uuid4()), 'items-TOTAL_FORMS': '1', 'items-INITIAL_FORMS': '1',
                'items-MIN_NUM_FORMS': '1', 'items-MAX_NUM_FORMS': '20',
                'items-0-product': str(self.product.pk), 'items-0-quantity': '0,500',
                'forms_count': '1', 'action': 'confirm', **changes}

    def test_every_operation_requires_login_and_permission(self):
        urls = ['/', '/produtos/', '/produtos/novo/', f'/produtos/{self.product.pk}/editar/',
                '/vendas/nova/', '/vendas/999/', '/historico/']
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 302)
                self.assertEqual(self.client.post(url, {}).status_code, 302)
        self.client.force_login(self.other, backend='django.contrib.auth.backends.ModelBackend')
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)
                self.assertEqual(self.client.post(url, {}).status_code, 403)

    def test_login_and_logout_invalidates_session(self):
        old = self.client.get('/entrar/')
        self.assertContains(old, 'Entrar')
        self.assertEqual(self.client.post('/entrar/', {'username': self.owner.username, 'password': TEST_PASSWORD}).status_code, 302)
        cookie = self.client.cookies['sessionid'].value
        self.assertEqual(self.client.get('/sair/').status_code, 405)
        self.assertEqual(self.client.post('/sair/').status_code, 302)
        replay = Client()
        replay.cookies['sessionid'] = cookie
        self.assertEqual(replay.get('/').status_code, 302)

    def test_invalid_login_generic(self):
        self.assertContains(self.client.post('/entrar/', {'username': 'desconhecido', 'password': 'wrong'}), 'Não foi possível entrar')
        self.assertEqual(self.client.get('/').status_code, 302)

    def test_hash_not_plain_or_weak(self):
        self.assertTrue(self.owner.password.startswith('pbkdf2_sha256$'))
        self.assertNotEqual(self.owner.password, TEST_PASSWORD)
        self.assertTrue(check_password(TEST_PASSWORD, self.owner.password))

    def test_rate_limit_and_cooloff(self):
        for _ in range(5):
            response = self.client.post('/entrar/', {'username': self.owner.username, 'password': 'wrong'})
        self.assertEqual(response.status_code, 429)
        self.assertContains(response, 'temporariamente bloqueado', status_code=429)
        self.assertEqual(self.client.post('/entrar/', {'username': self.owner.username, 'password': TEST_PASSWORD}).status_code, 429)
        AccessAttempt.objects.all().update(attempt_time=timezone.now() - timedelta(minutes=16))
        self.assertEqual(self.client.post('/entrar/', {'username': self.owner.username, 'password': TEST_PASSWORD}).status_code, 302)

    def test_csrf_required_and_valid_token_works(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner, backend='django.contrib.auth.backends.ModelBackend')
        self.assertEqual(client.post('/produtos/novo/', {}).status_code, 403)
        self.assertEqual(client.post('/vendas/nova/', self.sale_payload()).status_code, 403)
        client.get('/vendas/nova/')
        token = client.cookies['csrftoken'].value
        payload = self.sale_payload(csrfmiddlewaretoken=token)
        self.assertEqual(client.post('/vendas/nova/', payload).status_code, 302)
        self.assertEqual(Sale.objects.count(), 1)

    def test_expired_session(self):
        self.login()
        session = self.client.session
        session['last_activity'] = time.time() - 1801
        session.save()
        self.assertRedirects(self.client.get('/'), '/entrar/?expired=1')
        self.assertContains(self.client.get('/entrar/?expired=1'), 'sessão expirou')

    def test_active_session_and_headers(self):
        self.login()
        self.client.get('/')
        response = self.client.get('/')
        self.assertContains(response, 'Iniciar venda')
        self.assertIn('last_activity', self.client.session)
        self.assertEqual(response['Cache-Control'], 'no-store, private')
        self.assertIn("script-src 'none'", response['Content-Security-Policy'])
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertTrue(response.cookies['sessionid']['httponly'])
        self.assertEqual(response.cookies['sessionid']['samesite'], 'Lax')

    @override_settings(SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True)
    def test_secure_cookie_flags(self):
        self.login()
        response = self.client.get('/vendas/nova/', secure=True)
        self.assertTrue(response.cookies['sessionid']['secure'])
        self.assertTrue(response.cookies['csrftoken']['secure'])

    def test_product_create_edit_validation_and_inactive(self):
        self.login()
        self.assertContains(self.client.get('/produtos/novo/'), 'Cadastrar produto')
        data = {'name': 'Novo fictício', 'price': '4.20', 'stock': '4', 'unit': 'UN', 'active': 'on'}
        self.assertRedirects(self.client.post('/produtos/novo/', data), '/produtos/')
        product = Product.objects.get(name='Novo fictício')
        self.assertContains(self.client.get(f'/produtos/{product.pk}/editar/'), 'Editar produto')
        data['name'] = 'Editado'
        data.pop('active')
        self.assertRedirects(self.client.post(f'/produtos/{product.pk}/editar/', data), '/produtos/')
        product.refresh_from_db()
        self.assertFalse(product.active)
        data['name'] = '<script>alert(1)</script>'
        self.assertContains(self.client.post('/produtos/novo/', data), 'sem marcação HTML')
        self.assertContains(self.client.post(f'/produtos/{product.pk}/editar/', data), 'sem marcação HTML')

    def test_search_injection_and_pagination(self):
        self.login()
        Product.objects.bulk_create([Product(name=f'Item {i}', price=1, stock=1, unit='UN') for i in range(30)])
        response = self.client.get('/produtos/')
        self.assertEqual(len(response.context['page']), 25)
        self.assertContains(response, 'Próxima')
        self.assertContains(self.client.get('/produtos/?page=2'), 'Anterior')
        self.assertContains(self.client.get('/produtos/', {'q': "'; DROP TABLE loja_product;--"}), 'Nenhum produto encontrado')
        self.assertEqual(Product.objects.count(), 32)

    def test_stored_text_escaped_even_if_inserted_outside_form(self):
        self.login()
        Product.objects.filter(pk=self.product.pk).update(name='<script>alert(1)</script>')
        response = self.client.get('/produtos/')
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_sale_form_multi_rows_and_malformed_count(self):
        self.login()
        self.assertContains(self.client.get('/vendas/nova/?items=3'), 'Item 3')
        self.assertEqual(len(self.client.get('/vendas/nova/?items=bad').context['formset'].forms), 1)
        self.assertEqual(len(self.client.get('/vendas/nova/?items=999').context['formset'].forms), 20)

    def test_sale_preview_and_confirm_and_historical_unit_lock(self):
        self.login()
        payload = self.sale_payload(action='preview')
        preview = self.client.post('/vendas/nova/', payload)
        self.assertContains(preview, 'Total: R$ 10,00')
        self.assertFalse(Sale.objects.exists())
        payload['action'] = 'confirm'
        response = self.client.post('/vendas/nova/', payload)
        sale = Sale.objects.get()
        self.assertRedirects(response, reverse('sale_detail', args=[sale.pk]))
        self.assertContains(self.client.get(response.url), 'Venda registrada')
        self.assertContains(self.client.get('/historico/'), 'Conferir venda')
        self.assertTrue(self.client.get(f'/produtos/{self.product.pk}/editar/').context['form'].fields['unit'].disabled)
        self.assertEqual(self.client.post('/vendas/nova/', payload).url, response.url)
        self.assertEqual(Sale.objects.count(), 1)

    def test_sale_errors_and_database_failure(self):
        self.login()
        self.assertContains(self.client.post('/vendas/nova/', self.sale_payload(**{'items-0-quantity': '8'})), 'Estoque insuficiente')
        self.assertContains(self.client.post('/vendas/nova/', self.sale_payload(**{'items-0-quantity': '-1'})), 'errorlist')
        self.assertFalse(Sale.objects.exists())
        payload = self.sale_payload()
        with patch('loja.views.register_sale', side_effect=DatabaseError('private-database-detail')):
            response = self.client.post('/vendas/nova/', payload)
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, payload['operation_key'], status_code=503)
        self.assertNotContains(response, 'private-database-detail', status_code=503)

    def test_get_does_not_record_sale_and_missing_result_generic(self):
        self.login()
        self.client.get('/vendas/nova/')
        self.assertFalse(Sale.objects.exists())
        response = self.client.get('/vendas/9999/')
        self.assertContains(response, 'Página não encontrada', status_code=404)
        self.assertNotContains(response, 'Traceback', status_code=404)

    def test_no_open_redirect(self):
        response = self.client.post('/entrar/?next=https://malicioso.invalid', {'username': self.owner.username, 'password': TEST_PASSWORD})
        self.assertEqual(response.url, '/')

    def test_formset_tampering_rejected(self):
        self.login()
        response = self.client.post('/vendas/nova/', {'operation_key': str(uuid4()), 'items-TOTAL_FORMS': '99999'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Sale.objects.exists())

    def test_keyboard_and_labels_in_html(self):
        self.login()
        response = self.client.get('/vendas/nova/')
        self.assertContains(response, 'lang="pt-BR"')
        self.assertContains(response, 'Pular para o conteúdo')
        self.assertContains(response, 'for="id_items-0-quantity"')
        self.assertContains(response, '<fieldset>')
        self.assertContains(response, 'csrfmiddlewaretoken')
