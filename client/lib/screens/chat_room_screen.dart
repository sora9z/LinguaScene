import 'dart:convert';
import 'package:client/models/chat_room.dart';
import 'package:client/providers/chat_room_provider.dart';
import 'package:client/services/socket_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ChatRoomScreen extends StatefulWidget {
  final ChatRoom chatRoom;

  const ChatRoomScreen({super.key, required this.chatRoom});

  @override
  _ChatRoomScreenState createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends State<ChatRoomScreen> {
  final TextEditingController _messageController = TextEditingController();
  // final List<String> _messages = []; // 메시지 리스트
  late SocketService _socketService;

  @override
  void initState() {
    super.initState();
    _initializeSocketConnection();
  }

  Future<void> _initializeSocketConnection() async {
    final roomPk = widget.chatRoom.id;
    _socketService = SocketService(roomPk);
    await _socketService.createSocketConnection();

    // 소켓 메시지 수신 로직
    _socketService.channel?.stream.listen(
      (message) {
        print('Received message: $message');
        _addMessage(jsonDecode(message)['message'], false);
      },
      onDone: () {
        print('Disconnected from chat room $roomPk');
      },
      onError: (error) {
        print('Error: $error');
      },
    );
  }

  void _addMessage(String message, bool isMe) {
    if (isMe) {
      Provider.of<ChatRoomProvider>(context, listen: false)
          .addMessage('user-message', message);
      setState(() {});
    } else {
      Provider.of<ChatRoomProvider>(context, listen: false)
          .addMessage('gpt-message', message);
      setState(() {});
    }
  }

  void _sendMessage() {
    final message = _messageController.text.trim();
    if (message.isNotEmpty) {
      _addMessage(message, true);
      _messageController.clear();
      var userMessage = {'type': 'user-message', 'message': message};
      _socketService.sendMessage(userMessage);
    }
  }

  @override
  void dispose() {
    _socketService.closeConnection();
    _messageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.chatRoom.title ?? ''),
        backgroundColor: Colors.green,
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: Consumer<ChatRoomProvider>(
                builder: (context, chatRoomProvider, child) {
                  return ListView.builder(
                    reverse: true,
                    padding: const EdgeInsets.all(10),
                    itemCount: chatRoomProvider.messages.length,
                    itemBuilder: (context, index) {
                      final message = chatRoomProvider.messages[
                          chatRoomProvider.messages.length - 1 - index];
                      bool isGptMessage =
                          message.type == 'gpt-message'; // GPT 메시지 확인

                      return Row(
                        mainAxisAlignment: isGptMessage
                            ? MainAxisAlignment.start
                            : MainAxisAlignment.end,
                        children: [
                          if (isGptMessage) // gpt-message일 때만 표시
                            const Column(
                              children: [
                                CircleAvatar(
                                  backgroundColor: Colors.blue,
                                  child: Icon(Icons.account_circle,
                                      size: 30, color: Colors.white), // 배경 색상
                                ),
                                SizedBox(height: 5),
                                Text('Sora'), // GPT 이름
                              ],
                            ),
                          Container(
                            margin: const EdgeInsets.symmetric(
                                vertical: 5, horizontal: 8),
                            padding: const EdgeInsets.all(10),
                            constraints: BoxConstraints(
                              maxWidth: MediaQuery.of(context).size.width * 0.7,
                            ),
                            decoration: BoxDecoration(
                              color: isGptMessage
                                  ? Colors.blue[100]
                                  : Colors.yellow[100],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              message.message,
                              style: const TextStyle(fontSize: 16),
                            ),
                          ),
                          if (!isGptMessage) // user-message일 때만 표시
                            const Column(
                              children: [
                                Text('Me'), // 사용자 이름
                                SizedBox(height: 5),
                                CircleAvatar(
                                  backgroundColor: Colors.blue,
                                  child: Icon(Icons.account_circle,
                                      size: 30, color: Colors.white), // 배경 색상
                                ),
                              ],
                            ),
                        ],
                      );
                    },
                  );
                },
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                border: Border(top: BorderSide(color: Colors.grey[300]!)),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      decoration: const InputDecoration(
                        hintText: 'Enter your message',
                        border: InputBorder.none,
                      ),
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send, color: Colors.green),
                    onPressed: _sendMessage,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
