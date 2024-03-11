import stripe
from rest_framework import viewsets, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from materials.models import Course, Lesson
from materials.permissions import IsOwnerOrModerator
from materials.serializers import CourseSerializer, LessonSerializer

from .paginators import CoursePaginator
from .models import Subscription
from users.stripe_services import StripeService

stripe.api_key = settings.STRIPE_SECRET_KEY


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        stripe_product = StripeService.create_stripe_product(name=course.title, description=course.description)
        course.stripe_id = stripe_product['id']
        stripe_price = StripeService.create_stripe_price(product_id=stripe_product['id'],
                                                         unit_amount=course.price * 100)
        course.stripe_price_id = stripe_price['id']
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrModerator]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        stripe_product = StripeService.create_stripe_product(name=lesson.title, description=lesson.description)
        lesson.stripe_id = stripe_product['id']
        stripe_price = StripeService.create_stripe_price(product_id=stripe_product['id'],
                                                         unit_amount=lesson.price * 100)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CoursePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        course = get_object_or_404(Course, id=pk)
        subs_item, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            message = 'Подписка добавлена'
        else:
            subs_item.delete()
            message = 'Подписка удалена'

        return Response({"message": message})
