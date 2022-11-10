from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.profile_settings_url = reverse('profile settings')
        self.new_post_url = reverse('new post')
        self.delete_user_url = reverse('delete user')
        self.one_post_url = reverse('show one post', args=['1'])
        self.delete_post_url = reverse('delete post', args=['1'])
        self.user = {
            'email': 'test.email@gmail.com',
            'username': 'username',
            'first_name': 'John',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }
        self.image = SimpleUploadedFile(name='test_image.jpg',
                                        content=b'some_content',
                                        content_type='image/jpeg')
        self.profile_settings = {
            'username': 'username',
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'bio',
            'avatar': self.image
        }
        self.new_post = {
            'image': self.image,
            'tags': 'some tags'
        }
        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_GET_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_profile.html')

    def test_profile_GET_content_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.profile_url)
        assert b'username: username' in response.content

    def test_profile_GET_not_logged_in(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

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
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.new_post_url, self.new_post)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_GET_logged_in(self):
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_user.html')

    def test_delete_user_GET_not_logged_in(self):
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_user_POST(self):
        self.client.post(self.register_url, self.user)
        response = self.client.post(self.delete_user_url)
        self.assertEqual(response.status_code, 302)

    def test_show_one_post_GET_correctly(self):
        self.client.post(self.register_url, self.user)
        self.client.post(self.new_post_url, self.new_post)
        response = self.client.get(self.one_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_one_post.html')

    def test_show_one_post_GET_post_dont_exist(self):
        response = self.client.get(self.one_post_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_GET_logged_in_deletes_own_post(self):
        self.client.post(self.register_url, self.user)
        self.client.post(self.new_post_url, self.new_post)
        response = self.client.get(self.delete_post_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_GET_logged_in_deletes_someones_post(self):
        self.client.post(self.register_url, self.user)
        self.client.post(self.new_post_url, self.new_post)
        self.client.post(self.logout_url)
        self.client.post(self.register_url, self.user)
        response = self.client.get(self.delete_post_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_POST(self):
        self.client.post(self.register_url, self.user)
        self.client.post(self.new_post_url, self.new_post)
        response = self.client.post(self.delete_post_url)
        self.assertEqual(response.status_code, 302)