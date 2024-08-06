from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('create/', views.create_chat_room, name='create_chat_room'),
    path('join/', views.join_chat_room, name='join_chat_room'),
    path('create-or-join-room/', views.create_or_join_room, name='create_or_join_room'),
    path('room/<slug:slug>/', views.chat_room_view, name='chat_room'),
]
