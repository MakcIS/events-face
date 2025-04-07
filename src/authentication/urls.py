from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from src.authentication.views import CreateNewUser, LogoutView

urlpatterns = [
    path("register/", CreateNewUser.as_view(), name="new_user"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
