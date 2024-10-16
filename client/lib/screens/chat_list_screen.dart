import 'package:client/models/chat_room.dart';
import 'package:client/providers/chat_room_provider.dart';
import 'package:client/screens/chat_room_create_screen.dart';
import 'package:client/screens/chat_room_screen.dart';
import 'package:client/screens/login_screen.dart';
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

  @override
  void initState() {
    super.initState();
    _loadChatRooms();
  }

  Future<void> _loadChatRooms() async {
    try {
      final chatRooms = await _apiService.getChatRooms();
      Provider.of<ChatRoomProvider>(context, listen: false)
          .setChatRooms(chatRooms);
    } catch (e) {
      print('채팅방 목록을 불러오는데 실패했습니다: $e');
    }
  }

  void _navigateToChatRoomScreen(ChatRoom chatRoom) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ChatRoomScreen(chatRoom: chatRoom),
      ),
    );
  }

  void _navigateToChatRoomCreateScreen() async {
    await Navigator.push<ChatRoom>(
      context,
      MaterialPageRoute(builder: (context) => const ChatRoomCreateScreen()),
    );
  }

  void _logout() async {
    await _apiService.logout();
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (context) => const LoginScreen()),
      (Route<dynamic> route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('채팅 목록'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: Consumer<ChatRoomProvider>(
        builder: (context, chatRoomProvider, child) {
          return ListView.builder(
            itemCount: chatRoomProvider.chatRooms.length,
            itemBuilder: (context, index) {
              final chatRoom = chatRoomProvider.chatRooms[index];
              return Dismissible(
                key: Key(chatRoom.id.toString()),
                background: Container(
                  color: Colors.red,
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 20),
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                direction: DismissDirection.endToStart,
                onDismissed: (direction) async {
                  chatRoomProvider.removeChatRoom(chatRoom);
                  try {
                    await _apiService.deleteChatRoom(chatRoom.id);
                  } catch (error) {
                    print('채팅방 삭제 실패: $error');
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('채팅방 삭제에 실패했습니다: $error')),
                    );
                    chatRoomProvider.addChatRoom(chatRoom);
                  }
                },
                child: ListTile(
                  title: Text(chatRoom.title ?? '제목 없음'),
                  subtitle: Text(chatRoom.lastMessage ?? '메시지 없음'),
                  onTap: () => _navigateToChatRoomScreen(chatRoom),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _navigateToChatRoomCreateScreen,
        child: const Icon(Icons.add),
      ),
    );
  }
}
