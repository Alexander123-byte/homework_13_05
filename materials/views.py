from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsNotModer, IsOwnerOrModer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from .tasks import send_course_update_notification
from django.utils import timezone
from datetime import timedelta


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='description from swagger_auto_schema via method_decorator'
))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        send_course_update_notification.delay(instance.id)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, IsNotModer]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer, IsNotModer]
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwnerOrModer]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]

    def post(self, request, course_pk, lesson_pk, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_pk)
        lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Проверка времени последнего обновления курса
            if timezone.now() - course.last_updated > timedelta(hours=4):
                course.last_updated = timezone.now()
                course.save()

                # Получение подписчиков курса
                subscribers = Subscription.objects.filter(course=course)
                recipient_list = [sub.user.email for sub in subscribers]

                # Отправка email
                subject = 'Course Updated'
                message = f'The course "{course.title}" has been updated.'
                send_course_update_notification.delay(subject, message, recipient_list)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer, IsNotModer]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})

    def delete(self, request, course_id):
        subscription = get_object_or_404(
            Subscription, user=request.user, course_id=course_id
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
