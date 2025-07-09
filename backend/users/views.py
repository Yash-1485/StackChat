from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from authentication.utils.response import success_response, error_response
from authentication.models import User
from authentication.serializers import UserSerializer
from .models import FriendRequest
from .serializers import UserPublicSerializer, FriendRequestSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, id):
    try:
        sender = request.user

        if str(sender.id) == str(id):
            return error_response("You can't send a friend request to yourself", 400)

        recipient = User.objects.filter(id=id).first()
        if not recipient:
            return error_response("Recipient not found", 404)

        if sender.friends.filter(id=recipient.id).exists():
            return error_response("You are already friends with this user", 400)

        # Check if request already exists
        if FriendRequest.objects.filter(sender=sender, recipient=recipient, status='pending').exists():
            return error_response("Friend request already sent", 400)

        if FriendRequest.objects.filter(sender=recipient, recipient=sender, status='pending').exists():
            return error_response("User already sent you a friend request", 400)

        fr = FriendRequest.objects.create(sender=sender, recipient=recipient)
        return success_response(data=FriendRequestSerializer(fr).data, message="Friend request sent", status_code=201)

    except Exception as e:
        print("Error in send_friend_request:", str(e))
        return error_response("Internal Server Error", status_code=500)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, id):
    try:
        user = request.user
        friend_request = FriendRequest.objects.filter(id=id, status='pending').first()

        if not friend_request:
            return error_response("Friend request not found", 404)

        if friend_request.recipient != user:
            return error_response("You are not authorized to accept this request", 403)

        friend_request.status = "accepted"
        friend_request.save()

        user.friends.add(friend_request.sender)
        friend_request.sender.friends.add(user)

        return success_response(None, "Friend request accepted")

    except Exception as e:
        print("Error in accept_friend_request:", str(e))
        return error_response("Internal Server Error", 500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request):
    try:
        user = request.user

        incoming_requests = FriendRequest.objects.filter(
            recipient=user, status="pending"
        ).select_related('sender')

        accepted_requests = FriendRequest.objects.filter(
            sender=user, status="accepted"
        ).select_related('recipient')

        data = {
            "incomingReqs": FriendRequestSerializer(incoming_requests, many=True).data,
            "acceptedReqs": FriendRequestSerializer(accepted_requests, many=True).data
        }
        # return success_response(data, "Friend requests fetched")
        return Response(data, status=200)

    except Exception as e:
        print("Error in get_friend_requests:", str(e))
        return error_response("Internal Server Error", 500)

# We did this before
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_outgoing_friend_requests(request):
#     try:
#         user = request.user

#         outgoing_requests = FriendRequest.objects.filter(
#             sender=user, status="pending"
#         ).select_related('recipient')

#         data = FriendRequestSerializer(outgoing_requests, many=True).data
#         return success_response(data, "Outgoing friend requests fetched")

#     except Exception as e:
#         print("Error in get_outgoing_friend_requests:", str(e))
#         return error_response("Internal Server Error", 500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_outgoing_friend_requests(request):
    try:
        user = request.user

        # print("✅ Authenticated user:", user)

        outgoing_requests = FriendRequest.objects.filter(
            sender=user,
            status="pending"
        ).select_related("recipient")

        from users.serializers import FriendRequestSerializer
        serializer = FriendRequestSerializer(outgoing_requests, many=True)

        # print("✅ Outgoing friend requests:", serializer.data)

        # return success_response(serializer.data, "Outgoing friend requests fetched")
        return Response(serializer.data, status=200)

    except Exception as e:
        # import traceback
        # traceback.print_exc()
        return error_response("Internal Server Error", 500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_friends(request):
    try:
        user = request.user
        friends = user.friends.all()
        serializer = UserPublicSerializer(friends, many=True)
        # return success_response(serializer.data, "Your friends list")
        return Response(serializer.data, status=200)

    except Exception as e:
        print("Error in get_my_friends:", str(e))
        return error_response("Internal Server Error", 500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommended_users(request):
    try:
        user = request.user

        recommended = User.objects.exclude(
            id=user.id
        ).exclude(
            id__in=user.friends.all()
        ).filter(isOnboarded=True)

        serializer = UserPublicSerializer(recommended, many=True)
        # return success_response(serializer.data, "Recommended users")
        return Response(serializer.data, status=200)

    except Exception as e:
        print("Error in get_recommended_users:", str(e))
        return error_response("Internal Server Error", 500)
