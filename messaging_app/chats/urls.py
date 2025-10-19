from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageViewSet.as_view({'get': 'list'}), name='messages'),
    path('messages/create/', views.MessageViewSet.as_view({'post': 'create'}), name='create_message'),
    path('conversations/', views.ConversationViewSet.as_view({'get': 'list'}), name='conversations'),
    path('conversations/add', views.ConversationViewSet.as_view({ 'post': 'create'}), name='create-conversation')
]
