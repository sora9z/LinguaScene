import 'package:flutter/foundation.dart';

class Message {
  final String type;
  final String message;

  Message(this.type, this.message);
}

class ChatRoomProvider with ChangeNotifier {
  final List<Message> _messages = [];

  List<Message> get messages => _messages;

  void addMessage(String type, String message) {
    _messages.add(Message(type, message));
    notifyListeners();
  }

  void clearMessages() {
    _messages.clear();
    notifyListeners();
  }
}
