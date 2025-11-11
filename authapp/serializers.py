# authapp/serializers.py
# from rest_framework import serializers
# from django.contrib.auth.models import User

# class SignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=6)

#     class Meta:
#         model = User
#         fields = ("id", "username", "email", "password")

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data.get("email", ""),
#             password=validated_data["password"]
#         )
#         return user


# authapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
# ✅ NEW IMPORTS for email verification
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import re  # ✅ for password strength check


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    # ✅ NEW: custom validation for password strength
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", value):
            raise serializers.ValidationError("Password must include at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must include at least one special character.")
        return value

    def create(self, validated_data):
        # ✅ make user inactive until email verified
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            is_active=False  # ✅ NEW: deactivate until verified
        )

        # ✅ NEW: Generate verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = f"{settings.FRONTEND_URL}/verify-email?uid={uid}&token={token}"

        # ✅ NEW: Send verification email
        send_mail(
            subject="Verify your email address",
            message=f"Hello {user.username},\n\nPlease verify your email by clicking the link below:\n{verify_url}\n\nIf you didn’t request this, you can ignore this email.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return user

