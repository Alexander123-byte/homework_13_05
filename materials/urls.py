from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                             LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionAPIView)

app_name = 'materials'

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscription_manage"),
]

urlpatterns += router.urls
