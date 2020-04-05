from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

import tempfile
from random import randint
import boto3
from slugify import slugify

from .models import Event


rekognition = boto3.client("rekognition")


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


class UploadsTest(TestCase):
    def _create_image(self):
        from PIL import Image
 
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')
 
        return open(f.name, mode='rb')
    
    def setUp(self):
        self.image = self._create_image()
        staff_user = User.objects.create_user('user-1', password='user-1')
        staff_user.profile.is_organization = True
        staff_user.profile.save()

 
    def tearDown(self):
        self.image.close()

    def test_create_event(self):
        self.client.post(reverse('users:login'), {'username': 'user-1', 'password': 'user-1'})
        response = self.client.post(
            reverse('recognition:create_event'), 
            data = {'event_name': "Test Event", 'poster': self.image},
            follow = True
        )
        try:
            created_event = Event.objects.get(event_name="Test Event")
            self.assertEqual(created_event.event_name, "Test Event")
        except:
            self.fail("Event not created")

        self.assertIn("test-event", rekognition.list_collections()['CollectionIds'])
        rekognition.delete_collection(CollectionId="test-event")
