from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users-list/', views.users, name='users'),

    path('user/<str:id>/', views.detail_profile, name='detail_profile'),
    path('update-profile/<str:id>/', views.update_profile, name='update_profile'),
    path('searched/', views.search_users, name='search_user'),

    path('organizations-list/', views.organizations, name='organizations'),
    path('organizations/<uuid:org_id>/', views.organization_detail, name='organization_detail'),
    path('organizations/update/<uuid:org_id>/', views.update_organization, name='update_organization'),
    path('organizations/create/', views.create_organization, name='create_organization')
]