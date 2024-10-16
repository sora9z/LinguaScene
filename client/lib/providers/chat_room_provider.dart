import 'package:client/models/chat_room.dart';
import 'package:client/models/message.dart';
import 'package:flutter/foundation.dart';

class ChatRoomProvider with ChangeNotifier {
  final List<ChatRoom> _chatRooms = [];

  List<ChatRoom> get chatRooms => _chatRooms;

  List<Message> getMessages(int chatRoomId) {
    final chatRoom = _chatRooms.firstWhere((room) => room.id == chatRoomId);
    return chatRoom.getMessages();
  }

  void updateLastMessage(int chatRoomId, String message) {
    final chatRoom = _chatRooms.firstWhere((room) => room.id == chatRoomId);
    chatRoom.updateLastMessage(message);
    notifyListeners(); // 상태 변경 알림
  }

  void setChatRooms(List<ChatRoom> chatRooms) {
    _chatRooms.clear();
    _chatRooms.addAll(chatRooms);
    notifyListeners();
  }

  void addChatRoom(ChatRoom newChatRoom) {
    // _chatRooms.add(newChatRoom);
    _chatRooms.insert(0, newChatRoom); // 새 채팅방을 리스트의 맨 앞에 추가
    notifyListeners();
  }

  void addMessageToChatRoom(
      int? chatRoomId, String message, MessageRole messageRole) {
    final chatRoom = _chatRooms.firstWhere((room) => room.id == chatRoomId);
    chatRoom.addMessage(Message(role: messageRole, message: message));
    notifyListeners();
  }

  void addMessagesToChatRoom(int chatRoomId, List<Message> messages) {
    final chatRoom = _chatRooms.firstWhere((room) => room.id == chatRoomId);
    chatRoom.addMessages(messages);
    notifyListeners();
  }

  void removeChatRoom(ChatRoom chatRoom) {
    _chatRooms.removeWhere((room) => room.id == chatRoom.id);
    notifyListeners();
  }
}
