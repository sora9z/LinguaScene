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
  final _phoneNumberController = TextEditingController();
  final _usernameController = TextEditingController();
  final _apiService = ApiService();

  void _signup() async {
    if (_passwordController.text != _confirmPasswordController.text) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Signup failed'),
          content: const Text('Password and confirm password do not match'),
          actions: [
            TextButton(
              child: const Text('OK'),
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
          _usernameController.text);

      print('Signup success: $result');
      Navigator.pop(context);
    } catch (e) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Error'),
          content: Text(e.toString()),
          actions: [
            TextButton(
              child: const Text('OK'),
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
      appBar: AppBar(title: const Text('regisgter')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'email'),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _passwordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'password'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _confirmPasswordController,
              obscureText: true,
              decoration: const InputDecoration(labelText: 'conform password'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _usernameController,
              decoration: const InputDecoration(labelText: 'user name'),
            ),
            const SizedBox(
              height: 16,
            ),
            TextField(
              controller: _phoneNumberController,
              decoration: const InputDecoration(labelText: 'phon number'),
            ),
            const SizedBox(
              height: 16,
            ),
            ElevatedButton(
              onPressed: _signup,
              child: const Text('Register'),
            )
          ],
        ),
      ),
    );
  }
}
