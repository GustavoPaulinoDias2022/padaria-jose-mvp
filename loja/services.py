"""Regras de venda: autorização, decimais, concorrência, atomicidade e reenvio."""
import hashlib
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from uuid import UUID

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

from .models import Product, Sale, SaleItem


class SaleError(ValueError):
    pass


def can_operate(user):
    return user.is_authenticated and user.is_active and user.has_perm('loja.operate_shop')


def _normalize(rows):
    if not isinstance(rows, list) or not 1 <= len(rows) <= 20:
        raise SaleError('Informe de 1 a 20 itens.')
    result = {}
    for row in rows:
        try:
            product_id = int(row['product_id'])
            quantity = Decimal(str(row['quantity']).replace(',', '.'))
        except (KeyError, TypeError, ValueError, InvalidOperation):
            raise SaleError('Produto ou quantidade inválidos.') from None
        if product_id <= 0 or not quantity.is_finite() or quantity <= 0 or quantity > Decimal('999999999.999'):
            raise SaleError('Informe uma quantidade positiva e válida.')
        if quantity != quantity.quantize(Decimal('0.001')):
            raise SaleError('Use no máximo três casas decimais na quantidade.')
        if product_id in result:
            raise SaleError('Adicione cada produto uma única vez na venda.')
        result[product_id] = quantity
    return sorted(result.items())


def _price_items(items, products):
    details = []
    total = Decimal('0.00')
    for pk, quantity in items:
        product = products.get(pk)
        if not product or not product.active:
            raise SaleError('Produto inexistente ou inativo.')
        if product.unit == Product.Unit.UN and quantity != quantity.to_integral_value():
            raise SaleError('Produtos em UN exigem quantidade inteira.')
        if quantity > product.stock:
            raise SaleError(f'Estoque insuficiente para {product.name}. Disponível: {product.stock} {product.unit}.')
        subtotal = (product.price * quantity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        details.append((product, quantity, subtotal))
        total += subtotal
    if total <= 0 or total > Decimal('9999999999.99'):
        raise SaleError('O total da venda deve estar entre R$ 0,01 e R$ 9.999.999.999,99.')
    return details, total


def register_sale(*, user, operation_key, rows):
    if not can_operate(user):
        raise PermissionDenied
    try:
        key = UUID(str(operation_key))
    except (ValueError, TypeError, AttributeError):
        raise SaleError('Identificador da operação inválido.') from None
    items = _normalize(rows)
    fingerprint = hashlib.sha256(json.dumps([(pk, str(q.normalize())) for pk, q in items]).encode()).hexdigest()
    # Serializa operações do mesmo operador e resolve reenvios simultâneos da mesma chave.
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=user.pk)
        previous = Sale.objects.filter(operation_key=key).first()
        if previous:
            if previous.user_id != user.pk or previous.fingerprint != fingerprint:
                raise SaleError('A chave já foi utilizada com outra operação.')
            return previous
        products = {p.pk: p for p in Product.objects.select_for_update().filter(pk__in=[pk for pk, _ in items]).order_by('pk')}
        details, total = _price_items(items, products)
        sale = Sale.objects.create(user=user, operation_key=key, fingerprint=fingerprint, total=total)
        for product, quantity, subtotal in details:
            updated = Product.objects.filter(pk=product.pk, active=True, stock__gte=quantity).update(stock=F('stock') - quantity)
            if updated != 1:
                raise SaleError('O estoque mudou. Confira as quantidades e tente novamente.')
            SaleItem.objects.create(sale=sale, product=product, product_name=product.name, quantity=quantity,
                                    unit_price=product.price, unit=product.unit, subtotal=subtotal)
        return sale


def preview_sale(*, user, rows):
    """Calcula uma prévia sem persistir; confirmação sempre revalida os dados."""
    if not can_operate(user):
        raise PermissionDenied
    items = _normalize(rows)
    products = {p.pk: p for p in Product.objects.filter(pk__in=[pk for pk, _ in items])}
    details, total = _price_items(items, products)
    return {'items': [{'product': p, 'quantity': q, 'subtotal': s} for p, q, s in details], 'total': total}
