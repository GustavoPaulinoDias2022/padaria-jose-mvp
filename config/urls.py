from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from loja.forms import LoginForm

urlpatterns = [
    path('entrar/', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('sair/', LogoutView.as_view(), name='logout'),
    path('', include('loja.urls')),
]
