from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.stripe_services import StripeService


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_paid', 'lesson_paid', 'payment_method',)
    ordering_fields = ('date_payment',)


class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = StripeService.retrieve_stripe_session(session_id)
        if session is not None:
            return JsonResponse(session)
        else:
            return JsonResponse({"error": "Сессия не найдена или произошла непредвиденная ошибка"}, status=404)


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
