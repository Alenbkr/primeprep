from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import RegisterSerializer

# Вспомогательная функция, чтобы не дублировать код настройки куки
def set_refresh_cookie(response, token_string):
    response.set_cookie(
        key='refresh_token',
        value=token_string,
        httponly=True,                                  # Защита от JS-вирусов
        secure=settings.JWT_COOKIE_SECURE,              # True только для HTTPS (из settings.py)
        samesite='Lax',                                 # Защита от CSRF-атак
        max_age=7 * 24 * 60 * 60                        # 7 дней жизни куки
    )

# --- 1. РЕГИСТРАЦИЯ ---
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Генерируем первую пару токенов для нового юзера
            refresh = RefreshToken.for_user(user)
            
            # Отдаем фронтенду только Access токен в JSON
            response = Response({
                "user": {"username": user.username, "email": user.email},
                "access": str(refresh.access_token),
            }, status=201)
            
            # Прячем созданный Рефреш токен в куку
            set_refresh_cookie(response, str(refresh))
            return response
            
        return Response(serializer.errors, status=400)


# --- 2. ВХОД (ЛОГИН) ---
class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Родитеский класс проверяет пароль и генерирует пару токенов в JSON
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            refresh_token = response.data['refresh']
            
            # Стираем Рефреш из JSON, чтобы фронтенд его не видел
            del response.data['refresh']
            
            # Прячем Рефреш в куку
            set_refresh_cookie(response, refresh_token)
            
        return response


# --- 3. ОБНОВЛЕНИЕ ТОКЕНА (Через 15 минут) ---
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Автоматически вытаскиваем старый Рефреш токен из Заголовков (Кук) браузера
        refresh_token = request.cookies.get('refresh_token')
        
        if not refresh_token:
            raise InvalidToken("Refresh токен не найден в cookies")
            
        # Подкладываем токен в тело запроса для стандартного Django
        request.data['refresh'] = refresh_token
        
        # Django сжигает старый токен, заносит в blacklist и генерирует ПАРУ новых токенов
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            new_refresh_token = response.data['refresh']
            
            # Снова стираем НОВЫЙ Рефреш из JSON ответа
            del response.data['refresh']
            
            # Перезаписываем куку в браузере НОВЫМ Рефреш токеном на следующие 7 дней
            set_refresh_cookie(response, new_refresh_token)

        return response


# --- 4. ВЫХОД ---
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response({"detail": "Вы вышли из системы."})
        response.delete_cookie('refresh_token')
        return response
