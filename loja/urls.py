from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.products, name='products'),
    path('produtos/novo/', views.product_create, name='product_create'),
    path('produtos/<int:pk>/editar/', views.product_edit, name='product_edit'),
    path('vendas/nova/', views.sale_new, name='sale_new'),
    path('vendas/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('historico/', views.history, name='history'),
]
