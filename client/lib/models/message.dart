enum MessageRole {
  system,
  user,
  assistant;

  static MessageRole fromString(String value) {
    return MessageRole.values.firstWhere((role) => role.name == value);
  }

  @override
  String toString() => name;
}

// enum MessageType {
//   RequestUserMessage = 'request_user_message',
//   RequestSystemMessage = 'request_system_message',
//   RequestRecommendMessage = 'request_recommend_message',
//   ResponseAssistantMessage = 'response_assistant_message';

//   static MessageType fromString(String value) {
//     return MessageType.values.firstWhere((type) => type.name.toLowerCase() == value);
//   }

//   @override
//   String toString() => name.toLowerCase().replaceAll('request', 'request_').replaceAll('response', 'response_');
// }

class Message {
  final MessageRole role;
  final String message;

  Message({
    required this.role,
    required this.message,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    final messageObj = Message(
      role: MessageRole.fromString(json['role'] as String),
      message: json['content'],
    );

    return messageObj;
  }
}
