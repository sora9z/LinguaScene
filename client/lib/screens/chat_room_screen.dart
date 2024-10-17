import 'dart:convert';
import 'package:client/models/chat_room.dart';
import 'package:client/models/message.dart';
import 'package:client/providers/chat_room_provider.dart';
import 'package:client/services/socket_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:client/services/api_service.dart';

class ChatRoomScreen extends StatefulWidget {
  final ChatRoom chatRoom;

  const ChatRoomScreen({super.key, required this.chatRoom});

  @override
  _ChatRoomScreenState createState() => _ChatRoomScreenState();
}

class _ChatRoomScreenState extends State<ChatRoomScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ApiService _apiService = ApiService();
  late SocketService _socketService;

  @override
  void initState() {
    super.initState();
    _initializeSocketConnection();
    _initializeMessages();
  }

  Future<void> _initializeMessages() async {
    try {
      if (widget.chatRoom.messages.isEmpty) {
        final messages =
            await _apiService.fetchMessagesForChatRoom(widget.chatRoom.id);

        if (mounted) {
          setState(() {
            Provider.of<ChatRoomProvider>(context, listen: false)
                .addMessagesToChatRoom(widget.chatRoom.id, messages);
          });
        }
      }
    } catch (e) {
      print('Failed to load messages: $e');
    }
  }

  Future<void> _initializeSocketConnection() async {
    final roomPk = widget.chatRoom.id;
    _socketService = SocketService(roomPk);
    await _socketService.createSocketConnection();

    // 소켓 메시지 수신 로직
    _socketService.channel?.stream.listen(
      (message) {
        print('Received message: $message');

        final decodedMessage = jsonDecode(message);
        final messageType = decodedMessage['type'];
        final messageContent = decodedMessage['message']['content'];

        _addMessage(messageContent, messageType);
      },
      onDone: () {
        print('Disconnected from chat room $roomPk');
      },
      onError: (error) {
        print('Error: $error');
      },
    );
  }

  void _addMessage(String content, String messageType) {
    MessageRole messageRole;
    if (messageType == 'request_user_message' ||
        messageType == 'request_recommend_message') {
      messageRole = MessageRole.user;
    } else if (messageType == 'request_system_message') {
      messageRole = MessageRole.system;
    } else {
      messageRole = MessageRole.assistant;
    }

    Provider.of<ChatRoomProvider>(context, listen: false)
        .addMessageToChatRoom(widget.chatRoom.id, content, messageRole);

    Provider.of<ChatRoomProvider>(context, listen: false)
        .updateLastMessage(widget.chatRoom.id, content);
  }

  void _sendMessage() {
    final content = _messageController.text.trim();
    if (content.isNotEmpty) {
      var messageType = 'request_user_message';
      _addMessage(content, messageType);
      _messageController.clear();
      var userMessage = {'role': MessageRole.user.name, 'content': content};

      _socketService.sendMessage(messageType, userMessage);
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
        title: Column(
          children: [
            Text(widget.chatRoom.title ?? ''),
            Text(
              '${widget.chatRoom.language ?? '언어 없음'} - Level ${widget.chatRoom.level ?? '레벨 없음'}',
              style:
                  const TextStyle(fontSize: 12, fontWeight: FontWeight.normal),
            )
          ],
        ),
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
                    itemCount: widget.chatRoom.messages.length,
                    itemBuilder: (context, index) {
                      final message = widget.chatRoom.messages[
                          widget.chatRoom.messages.length - 1 - index];
                      bool isGptMessage = message.role == MessageRole.assistant;

                      return Row(
                        mainAxisAlignment: isGptMessage
                            ? MainAxisAlignment.start
                            : MainAxisAlignment.end,
                        children: [
                          if (isGptMessage) // assistant-message일 때만 표시
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
