import logging
from functools import wraps
from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm, SaleFormSet
from .models import Product, Sale
from .services import SaleError, can_operate, preview_sale, register_sale

logger = logging.getLogger(__name__)


def owner_required(view):
    @login_required
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not can_operate(request.user):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped


@owner_required
def home(request):
    return render(request, 'loja/home.html')


@owner_required
def products(request):
    query = request.GET.get('q', '')[:120]
    page = Paginator(Product.objects.filter(name__icontains=query), 25).get_page(request.GET.get('page'))
    return render(request, 'loja/products.html', {'page': page, 'query': query})


@owner_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('products')
    return render(request, 'loja/product_form.html', {'form': form})


@owner_required
def product_edit(request, pk):
    with transaction.atomic():
        product = get_object_or_404(Product.objects.select_for_update(), pk=pk)
        form = ProductForm(request.POST or None, instance=product)
        # Unidade não pode mudar depois de uma venda; preserva coerência do saldo.
        if product.saleitem_set.exists():
            form.fields['unit'].disabled = True
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('products')
    return render(request, 'loja/product_form.html', {'form': form, 'editing': True})


@owner_required
def sale_new(request):
    try:
        count = max(1, min(20, int(request.POST.get('forms_count', request.GET.get('items', '1')))))
    except (TypeError, ValueError):
        count = 1
    initial = [{} for _ in range(count)]
    formset = SaleFormSet(request.POST if request.method == 'POST' else None, initial=initial, prefix='items')
    key = request.POST.get('operation_key', str(uuid4()))
    error = None
    preview = None
    status = 200
    if request.method == 'POST' and formset.is_valid():
        rows = [{'product_id': f.cleaned_data['product'].pk, 'quantity': str(f.cleaned_data['quantity'])}
                for f in formset if f.cleaned_data]
        try:
            if request.POST.get('action') != 'confirm':
                preview = preview_sale(user=request.user, rows=rows)
            else:
                sale = register_sale(user=request.user, operation_key=key, rows=rows)
                return redirect('sale_detail', pk=sale.pk)
        except SaleError as exc:
            error = str(exc)
        except DatabaseError:
            logger.warning('Falha de persistência de venda; detalhes omitidos.')
            error = 'Não foi possível confirmar. Preserve esta página e tente novamente com a mesma operação; ela não será duplicada.'
            status = 503
    return render(request, 'loja/sale_form.html', {'formset': formset, 'operation_key': key,
                  'error': error, 'preview': preview, 'forms_count': count}, status=status)


@owner_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale.objects.select_related('user').prefetch_related('items__product'), pk=pk)
    return render(request, 'loja/sale_detail.html', {'sale': sale})


@owner_required
def history(request):
    page = Paginator(Sale.objects.select_related('user'), 25).get_page(request.GET.get('page'))
    return render(request, 'loja/history.html', {'page': page})
