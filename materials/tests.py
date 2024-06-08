from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group
from materials.models import Course, Lesson, Subscription
from users.models import User


class MaterialsApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@example.com", password="password")
        self.moderator = User.objects.create(
            email="moderator@example.com", password="password"
        )
        mod_group = Group.objects.create(name="moders")
        self.moderator.groups.add(mod_group)

        self.moderator.is_staff = True
        self.moderator.save()

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            course=self.course,
            owner=self.user,
            video_url="https://www.youtube.com/watch?v=test",
        )

    # CRUD Tests for Lessons
    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=newlesson",
        }
        response = self.client.post("/materials/lessons/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(title="New Lesson").exists())

    def test_update_lesson_by_moderator(self):
        self.client.force_authenticate(user=self.moderator)

        course = Course.objects.create(title="Test Course", owner=self.moderator)

        lesson = Lesson.objects.create(
            title="Test Lesson",
            course=course,
            owner=self.moderator,
            video_url="https://www.youtube.com/watch?v=test",
        )

        data = {
            "course": course.id,
            "title": "Updated Lesson Title",
            "description": "Updated Lesson Description",
            "video_url": "https://www.youtube.com/watch?v=updated",
        }

        response = self.client.put(
            f"/materials/lessons/{lesson.id}/update/", data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_by_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/materials/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post("/materials/subscriptions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.delete(f"/materials/subscriptions/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
