from django.contrib.auth import authenticate
from django.core.validators import validate_email
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullName', 'profilePic', 'bio', 'location', 'isOnboarded']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={
            "required": "Password is required",
            "min_length": "Password must be at least 8 characters long"
        }
    )

    email = serializers.EmailField(
        required=True,
        validators=[validate_email],  # Built-in Django email validation
        error_messages={
            'required': 'Email is required',
            'invalid': 'Invalid email address',
            'blank': 'Email cannot be blank'
        }
    )

    fullName = serializers.CharField(
        required=True,
        error_messages={"required": "Full name is required"}
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'fullName']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists, please use a different one",code="email_exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data["user"] = user
        return data

class OnboardingSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Full name is required",
            "blank": "Full name cannot be empty"
        }
    )
    bio = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Bio is required",
            "blank": "Bio cannot be empty"
        }
    )
    location = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Location is required",
            "blank": "Location cannot be empty"
        }
    )
    profilePic = serializers.URLField(
        required=False,
        allow_blank=True,
        error_messages={
            "invalid": "Profile picture must be a valid URL"
        }
    )

    class Meta:
        model = User
        fields = ['fullName', 'bio', 'location','profilePic']