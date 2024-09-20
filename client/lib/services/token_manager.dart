import 'package:shared_preferences/shared_preferences.dart';

class TokenManager {
  SharedPreferences? prefs;

  TokenManager() {
    _initPrefs();
  }

  Future<void> _initPrefs() async {
    prefs = await SharedPreferences.getInstance();
  }

  Future<void> saveTokens(String accessToken, String refreshToken) async {
    await prefs?.setString('accessToken', accessToken);
    await prefs?.setString('refreshToken', refreshToken);
  }

  Future<String?> getAccessToken() async {
    return prefs?.getString('accessToken');
  }

  Future<String?> getRefreshToken() async {
    return prefs?.getString('refreshToken');
  }

  Future<void> deleteTokens() async {
    await prefs?.remove('accessToken');
    await prefs?.remove('refreshToken');
  }
}
