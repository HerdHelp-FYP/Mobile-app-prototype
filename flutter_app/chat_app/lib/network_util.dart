import 'dart:io' as io;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:universal_io/io.dart';
import 'package:network_info_plus/network_info_plus.dart';

class NetworkUtil {
  static Future<String> getServerUrl() async {
    if (kIsWeb) {
      // For web, use a fixed public address or domain
      return 'http://localhost:5000';  // Replace with your web-compatible backend address
    } else {
      return await getLocalIpAddress();
    }
  }

  static Future<String> getLocalIpAddress() async {
    try {
      if (!kIsWeb && (io.Platform.isAndroid || io.Platform.isIOS || io.Platform.isLinux || io.Platform.isMacOS || io.Platform.isWindows)) {
        final info = NetworkInfo();
        String? wifiIP = await info.getWifiIP(); // Get the IP address for the Wi-Fi network
        if (wifiIP != null && wifiIP.isNotEmpty) {
          return wifiIP;
        }
      }
      throw Exception('Failed to get local IP address');
    } catch (e) {
      print('Error getting local IP address: $e');
      throw Exception('Failed to get local IP address');
    }
  }
}
