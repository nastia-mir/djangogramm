from django.test import SimpleTestCase, Client, TransactionTestCase, TestCase
from django.urls import reverse
import json
from .. import views
from ..models import DjGUser, Post, Image


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.testUser = DjGUser.objects.create(
            email='test.email@gmail.com',
            username='test.user',
            first_name='John',
            last_name='Doe',
        )
        return super().setUp()

    def test_home(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_profile.html')
