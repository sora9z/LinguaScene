class ChatRoomList {
  final int id;
  final String title;
  final String lastMessage;

  ChatRoomList({
    required this.id,
    required this.title,
    required this.lastMessage,
  });

  factory ChatRoomList.fromJson(Map<String, dynamic> json) {
    return ChatRoomList(
      id: json['id'] is int ? json['id'] : int.parse(json['id'].toString()),
      title: json['title'],
      lastMessage: json['last_message'],
    );
  }
}
