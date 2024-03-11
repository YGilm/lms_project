from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from materials.models import Course
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


class CreatePaymentSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        try:
            course = Course.objects.get(id=course_id)
            session = StripeService.create_stripe_session(
                price_id=course.stripe_price_id,
                success_url="http://example.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://example.com/cancel"
            )

            Payment.objects.create(
                user=user,
                course_paid=course,
                amount=course.price,
                id_stripe_session=session['id'],
                payment_method='card',  # Или другой метод
            )

            return Response({"session_url": session.url})
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


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
