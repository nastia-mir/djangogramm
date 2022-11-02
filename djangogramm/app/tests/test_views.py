from django.test import Client, TestCase
from django.urls import reverse
import json
from .. import views
from ..models import DjGUser, Post, Image


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.profile_settings_url = reverse('profile settings')
        self.new_post_url = reverse('new post')
        self.user = {
            'email': 'test.email@gmail.com',
            'username': 'username',
            'first_name': 'John',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }
        self.profile_settings = {
            'username': 'username',
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'bio',
            'avatar': 'avatar.jpg'
        }
        self.image = {'mugshot': SimpleUploadedFile('face.jpg', <file data>)}
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_profile.html')

    def test_profile_GET_content_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.profile_url)
        assert b'username: username' in response.content

    def test_profile_GET_content_not_logged_in(self):
        response = self.client.get(self.profile_url)
        assert b'You need to log in to access this page.' in response.content

    def test_profile_settings_GET_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_settings.html')

    def test_profile_settings_GET_not_logged_in(self):
        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_settings_POST(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.profile_settings_url, self.profile_settings)
        self.assertEqual(response.status_code, 200)

    def test_new_post_GET_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.new_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_post.html')

    def test_new_post_GET_not_logged_in(self):
        response = self.client.get(self.new_post_url)
        self.assertEqual(response.status_code, 302)

    def test_new_post_POST(self):





