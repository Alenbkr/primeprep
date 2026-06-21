from django.urls import path
from .views import RegisterView, CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]