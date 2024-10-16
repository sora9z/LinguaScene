import 'package:client/services/api_service.dart';
import 'package:flutter/material.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});
  @override
  _SignupScreenState createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _nameController = TextEditingController();
  final _phoneNumberController = TextEditingController();
  final _apiService = ApiService();

  void _signup() async {
    if (_passwordController.text != _confirmPasswordController.text) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('회원가입 실패'),
          content: const Text('비밀번호와 비밀번호 확인이 일치하지 않습니다.'),
          actions: [
            TextButton(
              child: const Text('확인'),
              onPressed: () => Navigator.of(context).pop(),
            )
          ],
        ),
      );
      return;
    }

    try {
      final result = await _apiService.signup(
        _emailController.text,
        _passwordController.text,
        _phoneNumberController.text,
        _nameController.text,
      );

      print('회원가입 성공: $result');
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('회원가입 성공'),
          content: Text(result['message'] ?? '회원가입이 완료되었습니다.'),
          actions: [
            TextButton(
              child: const Text('확인'),
              onPressed: () {
                Navigator.of(context).pop();
                Navigator.of(context).pop(); // 회원가입 화면을 닫습니다.
              },
            )
          ],
        ),
      );
    } catch (e) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('오류'),
          content: Text('회원가입 중 오류가 발생했습니다: ${e.toString()}'),
          actions: [
            TextButton(
              child: const Text('확인'),
              onPressed: () => Navigator.of(context).pop(),
            )
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('회원가입')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: '이메일'),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: '비밀번호'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _confirmPasswordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: '비밀번호 확인'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: '이름'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _phoneNumberController,
              decoration: const InputDecoration(labelText: '전화번호'),
            ),
            const SizedBox(
              height: 16,
            ),
            ElevatedButton(
              onPressed: _signup,
              child: const Text('회원가입'),
            )
          ],
        ),
      ),
    );
  }
}
