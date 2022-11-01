from django.test import Client, TestCase
from django.urls import reverse
from .. import views
from ..models import DjGUser


class TestAuth(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = {
            'email': 'test.email@gmail.com',
            'username': 'username',
            'first_name': 'John',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }
        self.user_login_data = {
            'email': 'test.email@gmail.com',
            'username': 'username',
            'first_name': 'John'
        }
        return super().setUp()

    def test_register_pageview(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 302)

    def test_register_used_email(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 200)
        assert b'This email is already used.' in response.content

    def test_login_pageview(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_user(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.login_url, self.user_login_data)
        print(response.content)
        self.assertEqual(response.status_code, 302)








    def test_logout_pageview(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)




