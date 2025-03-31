from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import CreateUserSerializer


class CreateNewUser(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            response = {
                "message": "User created successfully",
                "access_token": f"{access_token}",
                "refresh_token": f"{refresh_token}",
            }

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TokenRefreshSerializer

    def post(self, request: Request):
        token = request.data.get("refresh", None)
        if token is None:
            return Response(
                {"error": "Токен не передан"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(token)
            token.blacklist()
            return Response({"detail": "Вы успешно вышли"}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "Не верный токен"}, status=status.HTTP_401_UNAUTHORIZED
            )
