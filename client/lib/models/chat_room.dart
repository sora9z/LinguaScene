import 'package:client/models/message.dart';

class ChatRoom {
  final int id;
  final String? title; // 선택적 필드로 변경
  String? lastMessage; // 선택적 필드로 변경
  final String language;
  final int level;
  final String situation;
  final String situationEn;
  final String myRole;
  final String myRoleEn;
  final String gptRole;
  final String gptRoleEn;
  List<Message> messages;

  ChatRoom({
    required this.id,
    this.title, // 선택적 필드
    this.lastMessage, // 선택적 필드
    required this.language,
    required this.level,
    required this.situation,
    this.situationEn = '',
    required this.myRole,
    this.myRoleEn = '',
    required this.gptRole,
    this.gptRoleEn = '',
    this.messages = const [],
  });

  factory ChatRoom.fromJson(Map<String, dynamic> json) {
    return ChatRoom(
        id: json['id'] is int ? json['id'] : int.parse(json['id'].toString()),
        title: json['title'],
        lastMessage: json['last_message'],
        language: json['language'],
        level: json['level'] is int
            ? json['level']
            : int.parse(json['level'].toString()),
        situation: json['situation'],
        situationEn: json['situation_en'] ?? '',
        myRole: json['my_role'],
        myRoleEn: json['my_role_en'] ?? '',
        gptRole: json['gpt_role'],
        gptRoleEn: json['gpt_role_en'] ?? '',
        messages: json['messages'] ?? []);
  }

  void updateLastMessage(String message) {
    lastMessage = message;
  }

  List<Message> getMessages() {
    return messages;
  }

  void addMessage(Message message) {
    messages.add(message);
  }

  void addMessages(List<Message> newMessages) {
    messages.addAll(newMessages);
  }
}
