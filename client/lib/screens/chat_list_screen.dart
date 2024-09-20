import 'package:client/models/chat_room.dart';
import 'package:client/screens/chat_room_create_screen.dart';
import 'package:client/screens/chat_room_screen.dart';
import 'package:client/services/api_service.dart';
import 'package:flutter/material.dart';

class ChatListScreen extends StatefulWidget {
  const ChatListScreen({super.key});

  @override
  _ChatListScreenState createState() => _ChatListScreenState();
}

class _ChatListScreenState extends State<ChatListScreen> {
  final ApiService _apiService = ApiService();
  List<ChatRoom> _chatRooms = [];

  void _fetchChatRooms() async {
    try {
      List<ChatRoom> chatRooms = await _apiService.getChatRooms();
      setState(() {
        _chatRooms = chatRooms;
      });
    } catch (e) {
      print('Failed to load chat rooms: $e');
    }
  }

  @override
  void initState() {
    super.initState();
    _fetchChatRooms();
  }

  void _navigateToCreateChatRoom() {
    Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => const ChatRoomCreateScreen(),
        ));
  }

  String _truncateMessage(String message) {
    return message.length > 90 ? '${message.substring(0, 90)}...' : message;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat List'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _navigateToCreateChatRoom,
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: _chatRooms.length,
        itemBuilder: (context, index) {
          final chatRoom = _chatRooms[index];
          return ListTile(
            title: Text(chatRoom.title ?? ''),
            subtitle: Text(
                'Last meseage: ${_truncateMessage(chatRoom.lastMessage ?? '')}'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => ChatRoomScreen(chatRoom: chatRoom),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
