import 'package:client/services/token_manager.dart';
import 'package:client/services/api_service.dart';

class HttpHeaderBuilder {
  static final TokenManager _tokenManager = TokenManager();
  static final ApiService _apiService = ApiService();

  static Future<Map<String, String>> buildHeaders(
      {bool includeToken = true}) async {
    Map<String, String> headers = {
      'Content-Type': 'application/json',
    };

    if (includeToken) {
      if (await _tokenManager.isTokenExpired()) {
        final refreshSuccess = await _apiService.refreshToken();
        if (!refreshSuccess) {
          throw Exception('Session expired. Please login again.');
        }
      }

      final token = await _tokenManager.getAccessToken();
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      } else {
        throw Exception('No access token available.');
      }
    }

    return headers;
  }
}
