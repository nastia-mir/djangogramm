from django.test import SimpleTestCase, Client, TransactionTestCase
from django.urls import reverse
from .. import views
from ..models import DjGUser


class TestAuth(TransactionTestCase):

    def SetUp(self):
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

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')







    def test_logout_page(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)




    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 200)