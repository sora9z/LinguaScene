import 'package:shared_preferences/shared_preferences.dart';

class HttpHeaderBuilder {
  static Future<Map<String, String>> buildHeaders(
      {bool includeToken = true}) async {
    final prefs = await SharedPreferences.getInstance();
    Map<String, String> headers = {'Content-Type': 'application/json'};

    if (includeToken) {
      String? accessToken = prefs.getString('accessToken');
      if (accessToken != null) {
        headers['Authorization'] = 'Bearer $accessToken';
      }
    }

    return headers;
  }
}
