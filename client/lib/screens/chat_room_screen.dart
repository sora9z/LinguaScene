import 'package:client/models/chat_room.dart';
import 'package:flutter/material.dart';

class ChatRoomScreen extends StatefulWidget {
  final ChatRoom chatRoom;

  const ChatRoomScreen({super.key, required this.chatRoom});

  @override
  _ChatListScreenState createState() => _ChatListScreenState();
}

class _ChatListScreenState extends State<ChatRoomScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.chatRoom.title ?? ''),
      ),
      body: const Center(
          // TODO 채팅방 구현 예정
          child: Text('Chat room screen')),
    );
  }
}
