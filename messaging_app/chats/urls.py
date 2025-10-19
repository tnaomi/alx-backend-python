from django.urls import path
from . import views

urlpatterns = [
    path('', views.getChats, name='chat_list'),
    path('<str:chat_id>/', views.getChat, name='chat'),
]
