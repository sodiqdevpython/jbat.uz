from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('class-list/', views.class_list, name='class_list'),
    path('create-overall-class/', views.create_overall_class, name='create_overall_class'),
    path('delete-overall-class/<uuid:id>/', views.delete_overall_class, name='delete_overall_class'),

    path('create-room-type/', views.create_room_type, name='create_room_type'),
    path('delete-rooms-type/<uuid:id>/', views.delete_rooms_type, name='delete_rooms_type'),

    path('rooms-list/', views.room_list, name='rooms_list'),
    path('create-room', views.create_room, name='create_room'),
    path('delete-room/<uuid:id>/', views.delete_room, name='delete_room'),
    path('rooms/update/<uuid:id>/', views.update_room, name='update_room'),

    path('equipments-list/', views.equipment_list, name='equipment_list'),
    path('create-equipment/', views.create_equipment, name='create_equipment'),
    path('update-equipment/<uuid:pk>/', views.EquipmentUpdateView.as_view(), name='update_equipment'),
    path('delete-equipment/<uuid:id>/', views.delete_equipment, name='delete_equipment'),
    path('equipment/<uuid:pk>/', views.equipment_detail, name='equipment_detail'),
]