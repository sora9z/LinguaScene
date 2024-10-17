import 'package:shared_preferences/shared_preferences.dart';

class TokenManager {
  static const String _accessTokenKey = 'accessToken';
  static const String _refreshTokenKey = 'refreshToken';
  static const String _expirationTimeKey = 'expirationTime';
  SharedPreferences? _prefs;

  Future<void> _ensureInitialized() async {
    _prefs ??= await SharedPreferences.getInstance();
  }

  Future<void> saveTokens(
      String accessToken, String refreshToken, int expiresIn) async {
    await _ensureInitialized();

    await _prefs?.setString(_accessTokenKey, accessToken);
    await _prefs?.setString(_refreshTokenKey, refreshToken);
    await _prefs?.setInt(_expirationTimeKey, expiresIn * 1000);
  }

  Future<String?> getAccessToken() async {
    await _ensureInitialized();
    return _prefs?.getString(_accessTokenKey);
  }

  Future<String?> getRefreshToken() async {
    await _ensureInitialized();
    return _prefs?.getString(_refreshTokenKey);
  }

  Future<void> clearTokens() async {
    await _ensureInitialized();
    await _prefs?.remove(_accessTokenKey);
    await _prefs?.remove(_refreshTokenKey);
    await _prefs?.remove(_expirationTimeKey);
  }

  Future<bool> isTokenExpired() async {
    await _ensureInitialized();
    final expirationTime = _prefs?.getInt(_expirationTimeKey);
    if (expirationTime == null) return true;
    return DateTime.now().millisecondsSinceEpoch > expirationTime;
  }

  Future<bool> isTokenExpiringSoon() async {
    await _ensureInitialized();
    final expirationTime = _prefs?.getInt(_expirationTimeKey);
    if (expirationTime == null) return true;
    final now = DateTime.now().millisecondsSinceEpoch;
    // 만료 10분 전부터 알림
    return (expirationTime - now) < 600000 && (expirationTime - now) > 0;
  }
}
