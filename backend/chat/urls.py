from django.urls import path

from .views import ChatRoomCreateAPIView, ChatRoomDeleteAPIView, ChatRoomListAPIView

urlpatterns = [
    path('create/', ChatRoomCreateAPIView.as_view(), name='chatroom-create'),
    path('rooms/', ChatRoomListAPIView.as_view(), name='chatroom-list'),
    path('delete/<int:room_id>/', ChatRoomDeleteAPIView.as_view(), name='chatroom-delete'),
]