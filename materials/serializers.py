from rest_framework import serializers, generics
from materials.models import *
from materials.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[LinkValidator()])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, course=instance).exists()
