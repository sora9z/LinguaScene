from django.urls import path
from .views import ChatRoomCreateAPIView, ChatRoomListAPIView

urlpatterns = [
    path('create/', ChatRoomCreateAPIView.as_view(), name='chatroom-create'),
    path('rooms/', ChatRoomListAPIView.as_view(), name='chatroom-list'),
]