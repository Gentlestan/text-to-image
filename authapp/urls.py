# authapp/urls.py
# from django.urls import path
# from .views import SignupView, LoginView, LogoutView
# from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     path("signup/", SignupView.as_view(), name="signup"),
#     path("login/", LoginView.as_view(), name="login"),
#     path("logout/", LogoutView.as_view(), name="logout"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]

# authapp/urls.py
from django.urls import path
from .views import SignupView, LoginView, LogoutView, VerifyEmailView
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # ✅ Add this line
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]


