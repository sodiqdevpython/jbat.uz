from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def superuser_required(view_func):
    @login_required  # Foydalanuvchi login qilgan bo‘lishi shart
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:  # Faqat superuser ruxsati tekshiriladi
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Agar superuser bo‘lmasa, ruxsat yo‘qligini bildiradi

    return _wrapped_view
