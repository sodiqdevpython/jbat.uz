from django.urls import path
from . import views
from .decorators import superuser_required

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users-list/', superuser_required(views.users), name='users'),

    path('user/<str:id>/', superuser_required(views.detail_profile), name='detail_profile'),
    path('update-profile/<str:id>/', views.update_profile, name='update_profile'),
    path('searched/', views.search_users, name='search_user'),

    path('organizations-list/', superuser_required(views.organizations), name='organizations'),
    path('organizations/<uuid:org_id>/', superuser_required(views.organization_detail), name='organization_detail'),
    path('organizations/update/<uuid:org_id>/', superuser_required(views.update_organization), name='update_organization'),
    path('organizations/create/', superuser_required(views.create_organization), name='create_organization'),
    path('organization-delete/<uuid:org_id>/', superuser_required(views.delete_organization), name='delete_organization')
]