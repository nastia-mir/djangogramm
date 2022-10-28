from django.test import SimpleTestCase, Client, TransactionTestCase
from django.urls import reverse
import json
from .. import views
from ..models import DjGUser, Post, Image


class TestViews(TransactionTestCase):
    def SetUp(self):
        self.client = Client()
        self.testUser = DjGUser.objects.create(
            email='test.email@gmail.com',
            username='test.user',
            first_name='John',
            last_name='Doe',
        )

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_profile.html')
