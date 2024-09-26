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
