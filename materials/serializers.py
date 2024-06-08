from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from users.models import Payment
from materials.validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview_image", "video_url", "course"]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview_image",
            "description",
            "lessons",
            "lessons_count",
            "is_subscribed",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "course"]
