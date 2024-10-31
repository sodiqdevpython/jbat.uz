# myapp/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.utils import timezone

@receiver(user_logged_in)
def prevent_multiple_sessions(sender, request, user, **kwargs):
    # Foydalanuvchining barcha sessiyalarini olish
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in active_sessions:
        session_data = session.get_decoded()
        if session_data.get('_auth_user_id') == str(user.id):
            # Eski sessiyalarni o'chirish
            session.delete()
    # Yangi sessiya yaratish
    request.session.cycle_key()
