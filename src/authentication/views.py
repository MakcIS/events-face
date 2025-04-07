from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from src.authentication.serializer import CreateUserSerializer


class CreateNewUser(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        response = {
            "message": "User created successfully",
            "access_token": f"{access_token}",
            "refresh_token": f"{refresh_token}",
        }

        return Response(response, status=status.HTTP_201_CREATED)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenRefreshSerializer #Это только для документации

    def post(self, request: Request):
        try:
            token = request.data.get("refresh")
            token = RefreshToken(token)
            token.blacklist()

            return Response({"detail": "Вы успешно вышли"}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)