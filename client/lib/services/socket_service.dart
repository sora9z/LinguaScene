import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/io.dart';

class SocketService {
  IOWebSocketChannel? channel;
  final String baseUrl = 'ws://localhost:8000/ws/chat';
  final int roomPk;

  SocketService(this.roomPk); // 생성자를 통해 방 번호를 받는다

  Future<void> createSocketConnection() async {
    final prefs = await SharedPreferences.getInstance();
    String? accessToken = prefs.getString('accessToken');

    final uri = Uri.parse('$baseUrl/$roomPk/');
    channel = IOWebSocketChannel.connect(
      uri,
      headers: {
        'authorization': 'Bearer $accessToken', // JWT 토큰을 Authorization 헤더에 추가
      },
    );

    print('Connecting to chat room $roomPk');
  }

  void sendMessage(String type, Object content) {
    if (channel != null) {
      final jsonMessage = jsonEncode({'type': type, 'content': content});
      channel?.sink.add(jsonMessage);
      print("Sending message: $content");
    } else {
      print("WebSocket channel is not initialized. Cannot send message.");
    }
  }

  void closeConnection() {
    if (channel != null) {
      // channel?.sink.close(status.goingAway);
      channel?.sink.close(1000);
      print('Disconnected from chat room $roomPk');
    }
  }
}
