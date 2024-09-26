import 'dart:convert';
import 'package:client/models/chat_room.dart';
import 'package:client/models/message.dart';
import 'package:client/services/http_header_builder.dart';
import 'package:client/services/token_manager.dart';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://localhost:8000';
  final TokenManager tokenManager = TokenManager();

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login/'),
      headers: await HttpHeaderBuilder.buildHeaders(includeToken: false),
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      await tokenManager.saveTokens(data['accessToken'], data['refreshToken']);
      return data;
    } else {
      throw Exception('Failed to login');
    }
  }

  // 더미 데이터 생성을 위한 헬퍼 함수
  List<ChatRoom> _generateDummyChatRooms() {
    return List.generate(
      5,
      (index) => ChatRoom(
        id: index + 1,
        title: 'Chat Room ${index + 1}',
        lastMessage:
            'This is the last message in Chat Room ${index + 1}. It exceeds 100 characters.It exceeds 100 characters.It exceeds 100 characters.',
        language: 'English',
        level: 1,
        situation: 'Booking a hotel on the phone',
        myRole: 'Customer',
        gptRole: 'Hotel staff',
      ),
    );
  }

  Future<Map<String, dynamic>> signup(
    String email,
    String password,
    String phonNumber,
    String firstNeme,
    String lastName,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/signup/'),
      headers: await HttpHeaderBuilder.buildHeaders(includeToken: false),
      body: jsonEncode({
        'email': email,
        'password': password,
        'first_name': firstNeme,
        'last_name': lastName,
        'phone_number': phonNumber,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to signup');
    }
  }

  Future<List<ChatRoom>> getChatRooms() async {
    final response = await http.get(Uri.parse('$baseUrl/chat/rooms/'),
        headers: await HttpHeaderBuilder.buildHeaders());

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => ChatRoom.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load chat rooms');
    }
  }

  Future<ChatRoom> createChatRoom(Map<String, dynamic> chatRoomData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat/create/'),
      headers: await HttpHeaderBuilder.buildHeaders(),
      body: jsonEncode(chatRoomData),
    );

    if (response.statusCode == 201) {
      final data = ChatRoom.fromJson(jsonDecode(response.body));
      return data;
    } else {
      throw Exception('Failed to create chat room');
    }
  }

  Future<List<Message>> fetchMessagesForChatRoom(int chatRoomId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/message/messages/$chatRoomId/'),
      headers: await HttpHeaderBuilder.buildHeaders(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);

      final result = data
          .where((json) => json['role'] != MessageRole.system.name)
          .map((json) => Message.fromJson(json))
          .toList();

      return result;
    } else {
      throw Exception('Failed to load messages');
    }
  }

  Future<void> logout() async {
    final tokenManager = TokenManager();
    await tokenManager.clearTokens();
  }

  Future<bool> deleteChatRoom(int chatRoomId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/chat/delete/$chatRoomId/'),
      headers: await HttpHeaderBuilder.buildHeaders(),
    );

    if (response.statusCode == 200) {
      return true;
    } else {
      throw Exception('Failed to delete chat room');
    }
  }
}
