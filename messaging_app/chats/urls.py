from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='messages'),
    path('conversations/', views.ConversationViewSet.as_view({'get': 'list'}), name='conversations'),
]
