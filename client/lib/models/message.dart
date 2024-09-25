class Message {
  final String type;
  final String message;

  Message({
    required this.type,
    required this.message,
  });

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      type: json['role'],
      message: json['content'],
    );
  }
}
