from django.urls import path
from rest_framework import routers
from materials.apps import MaterialsConfig
from materials.views import *

app_name = MaterialsConfig.name
router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # subscribe
    path('subscribe/<int:pk>/', SubscriptionAPIView.as_view(), name='subscribe'),
] + router.urls

