from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class GeneralTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('recognition:index'))
        self.assertEqual(response.status_code, 200)


class EventsTest(TestCase):
    def test_event_page_ok(self):
        response = self.client.get(reverse('recognition:events'))
        self.assertEqual(response.status_code, 200)


class ProtectedUrlsTest(TestCase):
    def setUp(self):
        staff_user = User.objects.create_user('user-1', password='user-1')
        staff_user.profile.is_organization = True
        staff_user.profile.save()
        normal_user = User.objects.create_user('user-2', password='user-2')

    def test_create_event_route_staff(self):
        self.client.post(reverse('users:login'), {'username': 'user-1', 'password': 'user-1'})
        response = self.client.get(reverse('recognition:create_event'))
        self.assertEqual(response.status_code, 200)

    def test_create_event_route_normal_user(self):
        self.client.post(reverse('users:login'), {'username': 'user-2', 'password': 'user-2'})
        response = self.client.get(reverse('recognition:create_event'))
        self.assertEqual(response.status_code, 302)
