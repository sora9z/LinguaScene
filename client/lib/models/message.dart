class Message {
  final String type;
  final String message;

  Message({
    required this.type,
    required this.message,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    final messageObj = Message(
      type: json['role'] == 'user' || json['role'] == 'user-message'
          ? 'user-message'
          : 'assistant-message',
      message: json['content'],
    );

    return messageObj;
  }
}
