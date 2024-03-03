from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson

User = get_user_model()


class LessonTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user@example.com', password='password')

        self.admin_user = User.objects.create(
            email='admin@example.com',
            password='adminpassword',
            is_staff=True,
            is_superuser=True
        )
        self.admin_user.set_password('adminpassword')
        self.admin_user.save()
        self.client.force_authenticate(user=self.admin_user)

        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.admin_user)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Lesson Description',
                                            course=self.course, owner=self.admin_user)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'course': self.course.id
        }
        response = self.client.post('/materials/lesson/create/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/materials/lesson/')
        self.assertEqual(response.status_code, 200)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'course': self.course.id
        }
        response = self.client.put(f'/materials/lesson/{self.lesson.id}/update/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/materials/lesson/{self.lesson.id}/delete/')
        self.assertEqual(response.status_code, 204)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/materials/subscribe/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)




