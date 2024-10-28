from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-user/', views.create_profile, name='add_user'),
    path('delete/<str:passport_id>/', views.delete_user, name='delete_user')
]