from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, CreateUserView, PaymentStatusAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Payment
    path('payment/', PaymentListAPIView.as_view(), name='платежи'),
    path('payment-status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='статус-платежа'),

    # API Token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registration
    path('register/', CreateUserView.as_view(), name='user-register'),
]
