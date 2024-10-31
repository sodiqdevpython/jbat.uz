# myapp/middleware.py
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.utils import timezone

class OneActiveSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Foydalanuvchi tizimga kirganini tekshiramiz
        if request.user.is_authenticated:
            # Foydalanuvchining aktiv sessiyalarini olamiz
            user_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key=request.session.session_key
            )

            # Agar boshqa aktiv sessiya bo‘lsa, foydalanuvchini logout qilamiz
            if user_sessions.exists() and user_sessions.first().session_key != request.session.session_key:
                logout(request)

        response = self.get_response(request)
        return response
