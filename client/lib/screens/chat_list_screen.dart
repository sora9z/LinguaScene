import 'package:client/models/chat_room.dart';
import 'package:client/providers/chat_room_provider.dart';
import 'package:client/screens/chat_room_create_screen.dart';
import 'package:client/screens/chat_room_screen.dart';
import 'package:client/screens/login_screen.dart';
import 'package:client/services/api_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import 'package:client/services/token_manager.dart';

class ChatListScreen extends StatefulWidget {
  const ChatListScreen({super.key});

  @override
  _ChatListScreenState createState() => _ChatListScreenState();
}

class _ChatListScreenState extends State<ChatListScreen> {
  final ApiService _apiService = ApiService();
  final TokenManager _tokenManager = TokenManager();
  Timer? _tokenCheckTimer;

  @override
  void initState() {
    super.initState();
    _loadChatRooms();
    _startTokenCheck();
  }

  void _startTokenCheck() {
    _tokenCheckTimer = Timer.periodic(const Duration(minutes: 1), (timer) {
      _checkTokenExpiration();
    });
  }

  Future<void> _checkTokenExpiration() async {
    if (await _tokenManager.isTokenExpiringSoon()) {
      _showRefreshTokenDialog();
    }
  }

  void _showRefreshTokenDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('로그인 세션 만료'),
          content: const Text('로그인 세션이 곧 만료됩니다. 연장하시겠습니까?'),
          actions: <Widget>[
            TextButton(
              child: const Text('취소'),
              onPressed: () {
                Navigator.of(context).pop();
                _logout(); // 취소 시 로그아웃
              },
            ),
            TextButton(
              child: const Text('연장'),
              onPressed: () async {
                Navigator.of(context).pop();
                final success = await _apiService.refreshToken();
                if (success) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('로그인 세션이 연장되었습니다.')),
                  );
                } else {
                  _handleSessionExpired();
                }
              },
            ),
          ],
        );
      },
    );
  }

  @override
  void dispose() {
    _tokenCheckTimer?.cancel();
    super.dispose();
  }

  Future<void> _loadChatRooms() async {
    try {
      final chatRooms = await _apiService.getChatRooms();
      Provider.of<ChatRoomProvider>(context, listen: false)
          .setChatRooms(chatRooms);
    } catch (e) {
      if (e.toString().contains('Session expired')) {
        print('세션이 만료되었습니다: $e');
        _handleSessionExpired();
      } else {
        print('채팅방 목록을 불러오는데 실패했습니다: $e');
      }
    }
  }

  void _handleSessionExpired() {
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (context) => const LoginScreen()),
      (Route<dynamic> route) => false,
    );
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
    _handleSessionExpired(); // 로그아웃 후 로그인 화면으로 이동
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title:
            const Text('채팅 목록', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: Consumer<ChatRoomProvider>(
        builder: (context, chatRoomProvider, child) {
          return ListView.separated(
            itemCount: chatRoomProvider.chatRooms.length,
            separatorBuilder: (context, index) => const Divider(height: 1),
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
                  contentPadding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  leading: CircleAvatar(
                    backgroundColor: Colors.blue,
                    child: Text(
                      chatRoom.title?[0] ?? '?',
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                  title: Text(
                    chatRoom.title ?? '제목 없음',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const SizedBox(height: 4),
                      Text(
                        chatRoom.lastMessage != null &&
                                chatRoom.lastMessage!.length > 50
                            ? '${chatRoom.lastMessage!.substring(0, 50)}...'
                            : chatRoom.lastMessage ?? '메시지 없음',
                        style: TextStyle(color: Colors.grey[600]),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          Icon(Icons.language,
                              size: 16, color: Colors.blue[300]),
                          const SizedBox(width: 4),
                          Text(
                            chatRoom.language ?? '언어 없음',
                            style: TextStyle(
                                color: Colors.blue[300], fontSize: 12),
                          ),
                          const SizedBox(width: 8),
                          Icon(Icons.star, size: 16, color: Colors.amber[300]),
                          const SizedBox(width: 4),
                          Text(
                            'Level ${chatRoom.level ?? '?'}',
                            style: TextStyle(
                                color: Colors.amber[300], fontSize: 12),
                          ),
                        ],
                      ),
                    ],
                  ),
                  onTap: () => _navigateToChatRoomScreen(chatRoom),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _navigateToChatRoomCreateScreen,
        backgroundColor: Colors.blue,
        child: const Icon(Icons.add),
      ),
    );
  }
}
