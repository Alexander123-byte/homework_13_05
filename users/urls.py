from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, PaymentCreateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import UserCreateAPIView

app_name = "users"

router = DefaultRouter()
# router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("payments/", PaymentCreateAPIView.as_view(), name="payment"),
]
