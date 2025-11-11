# # authapp/views.py
# from rest_framework import generics, status, permissions
# from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from rest_framework.views import APIView
# from .serializers import SignupSerializer
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# class SignupView(generics.CreateAPIView):
#     serializer_class = SignupSerializer
#     permission_classes = [permissions.AllowAny]

# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if not user:
#             return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         # Set HttpOnly refresh token cookie
#         response = Response({
#             "access": access_token,
#             "user": {"id": user.id, "username": user.username, "email": user.email}
#         }, status=status.HTTP_200_OK)

#         # cookie settings - adjust secure=True in production (HTTPS)
#         response.set_cookie(
#             key="refresh_token",
#             value=refresh_token,
#             httponly=True,
#             secure=False,          # set True in production (https)
#             samesite="Lax",
#             max_age=7 * 24 * 60 * 60,  # matches refresh token lifetime
#             path="/api/auth/token/refresh/"  # optional: limit cookie to refresh endpoint
#         )
#         return response

# class LogoutView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         # We expect refresh token to be in cookies (HttpOnly) OR client can send it in body
#         refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
#         if not refresh_token:
#             return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh_token)
#             # blacklist the token (requires token_blacklist app)
#             token.blacklist()
#         except Exception:
#             # token invalid or already blacklisted — ignore
#             pass

#         # clear cookie
#         response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
#         response.delete_cookie("refresh_token", path="/api/auth/token/refresh/")
#         return response


# authapp/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .serializers import SignupSerializer



User = get_user_model()


# SIGNUP
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


# ✅ NEW: VERIFY EMAIL VIEW
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        uidb64 = request.query_params.get("uid")
        token = request.query_params.get("token")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Email verified successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# LOGIN
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ check if user is verified
        if not user.is_active:
            return Response({"detail": "Please verify your email before logging in."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "access": access_token,
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }, status=status.HTTP_200_OK)

        # cookie settings - adjust secure=True in production (HTTPS)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/api/auth/token/refresh/"
        )
        return response


# LOGOUT
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token") or request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token", path="/api/auth/token/refresh/")
        return response
