import 'package:client/providers/chat_room_provider.dart';
import 'package:client/screens/chat_list_screen.dart';
import 'package:client/screens/login_screen.dart';
import 'package:client/screens/signup_screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => ChatRoomProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lingua scene',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignupScreen(),
        '/chatsList': (context) => const ChatListScreen(),
      },
      home: const LoginScreen(),
    );
  }
}
