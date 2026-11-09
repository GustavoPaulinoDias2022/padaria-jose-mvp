import time

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        expired = False
        if request.user.is_authenticated:
            now = time.time()
            previous = request.session.get('last_activity', now)
            if now - previous >= 1800:
                logout(request)
                expired = True
            else:
                request.session['last_activity'] = now
        response = redirect(reverse('login') + '?expired=1') if expired else self.get_response(request)
        response['Content-Security-Policy'] = (
            "default-src 'self'; script-src 'none'; style-src 'self'; img-src 'self'; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
        )
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        if request.user.is_authenticated or expired:
            response['Cache-Control'] = 'no-store, private'
        return response
