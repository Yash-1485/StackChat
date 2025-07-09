from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.stream import generate_stream_token

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stream_token(request):
    try:
        user_id = str(request.user.id)
        token = generate_stream_token(user_id)
        # print(user_id)
        return Response({"token": token}, status=200)
    except Exception as e:
        print("Error in get_stream_token:", str(e))
        return Response({"message": "Internal Server Error"}, status=500)