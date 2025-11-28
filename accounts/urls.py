from django.urls import path
from .views import RegisterView, PasswordResetRequestView, SetNewPasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('set-password/', SetNewPasswordView.as_view(), name='set_password'),
]
