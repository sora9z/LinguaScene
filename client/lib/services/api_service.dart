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
    String phoneNumber,
    String name,
  ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/signup/'),
      headers: await HttpHeaderBuilder.buildHeaders(includeToken: false),
      body: jsonEncode({
        'email': email,
        'password': password,
        'phone_number': phoneNumber,
        'name': name,
      }),
    );

    if (response.statusCode == 201) {
      if (response.body.isEmpty) {
        return {'message': 'Signup successful'};
      }
      try {
        return jsonDecode(response.body);
      } catch (e) {
        print('Error decoding response: ${response.body}');
        return {
          'message': 'Signup successful, but response format is unexpected'
        };
      }
    } else {
      throw Exception('Failed to signup: ${response.body}');
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
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat/create/'),
        headers: await HttpHeaderBuilder.buildHeaders(),
        body: jsonEncode(chatRoomData),
      );

      if (response.statusCode == 201) {
        if (response.body.isEmpty) {
          throw Exception('서버에서 빈 응답을 반환했습니다.');
        }
        try {
          final data = ChatRoom.fromJson(jsonDecode(response.body));
          print('Created chat room: $data');
          return data;
        } catch (e) {
          print('JSON 디코딩 오류: $e');
          throw Exception('응답을 파싱하는 데 실패했습니다: $e');
        }
      } else {
        throw Exception(
            '채팅방 생성 실패. 상태 코드: ${response.statusCode}, 응답: ${response.body}');
      }
    } catch (e) {
      throw Exception('채팅방 생성 실패: $e');
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
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/chat/delete/$chatRoomId/'),
        headers: await HttpHeaderBuilder.buildHeaders(),
      );

      if (response.statusCode == 201) {
        return true;
      } else {
        throw Exception('Failed to delete chat room');
      }
    } catch (e) {
      throw Exception('Failed to delete chat room: $e');
    }
  }
}
