from rest_framework import serializers
from authentication.models import User
from .models import FriendRequest

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullName', 'profilePic', 'bio']

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserPublicSerializer(read_only=True)
    recipient = UserPublicSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'recipient', 'status', 'createdAt']
