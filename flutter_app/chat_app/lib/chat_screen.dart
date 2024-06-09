import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'network_util.dart'; // Import the utility class

// Chat model for storing messages
class ChatMessage {
  final String message;
  final bool isUser;

  ChatMessage({required this.message, required this.isUser});
}

// ChatProvider for managing chat state
class ChatProvider with ChangeNotifier {
  List<ChatMessage> _messages = [];

  List<ChatMessage> get messages => _messages;

  Future<void> sendMessage(String prompt, String sessionId) async {
    try {
      // Fetch the server URL using the utility function
      String serverUrl = await NetworkUtil.getServerUrl();
      final response = await http.post(
        Uri.parse('$serverUrl/api/query'), // Use the fetched server URL
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': prompt, 'session_id': sessionId}),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        final responseMessage = responseData['response'];
        _messages.add(ChatMessage(message: prompt, isUser: true));
        _messages.add(ChatMessage(message: responseMessage, isUser: false));
        notifyListeners();
      } else {
        throw Exception('Failed to load response');
      }
    } catch (e) {
      print('Error: $e');
      _messages.add(ChatMessage(message: 'Error: $e', isUser: false));
      notifyListeners();
    }
  }
}

// Main Chat Screen
class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final String sessionId = '1111';  // Example session ID

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat with Vet'),
      ),
      body: Column(
        children: [
          Expanded(
            child: Consumer<ChatProvider>(
              builder: (context, chatProvider, child) {
                return ListView.builder(
                  itemCount: chatProvider.messages.length,
                  itemBuilder: (context, index) {
                    final message = chatProvider.messages[index];
                    return ListTile(
                      title: Align(
                        alignment: message.isUser ? Alignment.centerRight : Alignment.centerLeft,
                        child: Container(
                          padding: EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: message.isUser ? Colors.blue : Colors.grey[300],
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Text(
                            message.message,
                            style: TextStyle(color: message.isUser ? Colors.white : Colors.black),
                          ),
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type your message here...',
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () async {
                    if (_controller.text.isNotEmpty) {
                      await Provider.of<ChatProvider>(context, listen: false).sendMessage(_controller.text, sessionId);
                      _controller.clear();
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
