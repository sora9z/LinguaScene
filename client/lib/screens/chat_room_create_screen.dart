import 'package:client/providers/chat_room_provider.dart';
import 'package:client/screens/chat_room_screen.dart';
import 'package:client/services/api_service.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ChatRoomCreateScreen extends StatefulWidget {
  const ChatRoomCreateScreen({super.key});

  @override
  _ChatRoomCreateScreenState createState() => _ChatRoomCreateScreenState();
}

class _ChatRoomCreateScreenState extends State<ChatRoomCreateScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _situationController = TextEditingController();
  final TextEditingController _myRoleController = TextEditingController();
  final TextEditingController _gptRoleController = TextEditingController();

  String? _selectedLanguage;
  int? _selectedLevel;

  final List<Map<String, dynamic>> _languages = [
    {'code': 'en-US', 'name': 'English'},
    {'code': 'ko-KR', 'name': 'Korean'},
    {'code': 'ja-JP', 'name': 'Japanese'},
    {'code': 'zh-CN', 'name': 'Chinese'},
    {'code': 'es-ES', 'name': 'Spanish'},
    {'code': 'fr-FR', 'name': 'French'},
    {'code': 'de-DE', 'name': 'German'},
    {'code': 'it-IT', 'name': 'Italian'},
    {'code': 'pt-PT', 'name': 'Portuguese'},
    {'code': 'ru-RU', 'name': 'Russian'},
    {'code': 'th-TH', 'name': 'Thai'},
  ];

  final List<Map<String, dynamic>> _levels = [
    {'code': 1, 'name': 'Beginner'},
    {'code': 2, 'name': 'Intermediate'},
    {'code': 3, 'name': 'Advanced'},
  ];

  void _createChatRoom() async {
    try {
      final newChatRoom = await _apiService.createChatRoom({
        'level': _selectedLevel,
        'language': _selectedLanguage,
        'title': _titleController.text,
        'situation': _situationController.text,
        'my_role': _myRoleController.text,
        'gpt_role': _gptRoleController.text,
      });

      Provider.of<ChatRoomProvider>(context, listen: false)
          .addChatRoom(newChatRoom);
      // 채팅방 화면으로 이동
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ChatRoomScreen(chatRoom: newChatRoom),
        ),
      );
    } catch (e) {
      print('새 채팅방 생성 실패: $e');
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('오류'),
          content: const Text('채팅방 생성 중 오류가 발생했습니다'),
          actions: [
            TextButton(
              child: const Text('확인'),
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create chat room'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: <Widget>[
            InputDecorator(
              decoration: InputDecoration(
                labelText: 'Select Language',
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(5.0)),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
                  value: _selectedLanguage,
                  isExpanded: true,
                  items: _languages.map((language) {
                    return DropdownMenuItem<String>(
                      value: language['code'],
                      child: Text(language['name']),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedLanguage = value;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 20),
            InputDecorator(
              decoration: InputDecoration(
                labelText: 'Select Level',
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(5.0)),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<int>(
                  value: _selectedLevel,
                  isExpanded: true,
                  items: _levels.map((level) {
                    return DropdownMenuItem<int>(
                      value: level['code'],
                      child: Text(level['name']),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedLevel = value;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(
                labelText: 'Title',
                hintText: '(optional)Hotel Reservation',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _situationController,
              decoration: const InputDecoration(
                labelText: 'Situation',
                hintText: '전화로 호텔 방 예약하기',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _myRoleController,
              decoration: const InputDecoration(
                labelText: 'My Role',
                hintText: '손님',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: _gptRoleController,
              decoration: const InputDecoration(
                labelText: 'GPT Role',
                hintText: '호텔 직원',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _createChatRoom,
              child: const Text('Create chat room'),
            ),
          ],
        ),
      ),
    );
  }
}
