import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'chat_screen.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ChatProvider(),
      child: MaterialApp(
        title: 'Flutter Chat App',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: ChatScreen(),
      ),
    );
  }
}
