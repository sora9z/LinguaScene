import 'package:client/models/chat_room.dart';
import 'package:client/providers/chat_room_provider.dart';
import 'package:client/screens/chat_room_create_screen.dart';
import 'package:client/screens/chat_room_screen.dart';
import 'package:client/services/api_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ChatListScreen extends StatefulWidget {
  const ChatListScreen({super.key});

  @override
  _ChatListScreenState createState() => _ChatListScreenState();
}

class _ChatListScreenState extends State<ChatListScreen> {
  final ApiService _apiService = ApiService();

  void _fetchChatRooms() async {
    try {
      List<ChatRoom> chatRooms = await _apiService.getChatRooms();
      setState(() {
        Provider.of<ChatRoomProvider>(context, listen: false)
            .setChatRooms(chatRooms);
      });
    } catch (e) {
      print('Failed to load chat rooms: $e');
    }
  }

  void _logout() async {
    try {
      await _apiService.logout();
      Navigator.of(context).pushReplacementNamed('/login');
    } catch (e) {
      print('Failed to logout: $e');
    }
  }

  Future<void> _deleteChatRoom(ChatRoom chatroom) async {
    try {
      await _apiService.deleteChatRoom(chatroom.id);
      setState(() {
        Provider.of<ChatRoomProvider>(context, listen: false)
            .removeChatRoom(chatroom);
      });
    } catch (e) {
      print('Failed to delete chatRoomL $e');
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
        automaticallyImplyLeading: false, // 뒤로 가기 버튼 숨기기
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _navigateToCreateChatRoom,
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: Provider.of<ChatRoomProvider>(context).chatRooms.length,
        itemBuilder: (context, index) {
          final chatRoom =
              Provider.of<ChatRoomProvider>(context).chatRooms[index];
          return ListTile(
            title: Row(
              children: [
                Expanded(
                  child: Text(chatRoom.title ?? ''),
                ),
                GestureDetector(
                    onTap: () => _deleteChatRoom(chatRoom),
                    child: const Text('Delete',
                        style: TextStyle(
                          decoration: TextDecoration.underline,
                          color: Colors.red,
                        )))
              ],
            ),
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
