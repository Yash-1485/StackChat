from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get('token')

            if not token:
                raise AuthenticationFailed("Unauthorized - No token provided")

            try:
                validated_token = self.get_validated_token(token)
            except Exception:
                raise AuthenticationFailed("Unauthorized - Invalid token")

            user = self.get_user(validated_token)
            if not user:
                raise AuthenticationFailed("Unauthorized - User not found")

            return (user, validated_token)
        except Exception as e:
            # raise AuthenticationFailed("Error while validating JWT token")
            print(f"Error during JWT authentication middleware: {str(e)}")