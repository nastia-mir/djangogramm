from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from ..models import DjGUser


class TestViewsLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.profile_settings_url = reverse('profile settings')
        self.new_post_url = reverse('new post')
        self.delete_user_url = reverse('delete user')
        self.one_post_url = reverse('show one post', args=['1'])
        self.post_dont_exist_url = reverse('show one post', args=['10'])
        self.delete_post_url = reverse('delete post', args=['1'])
        self.like_post_url = reverse('like', args=['1'])
        self.unlike_post_url = reverse('unlike', args=['1'])
        self.show_likes_url = reverse('show likes', args=['1'])
        self.follow_url = reverse('follow', args=['2'])
        self.unfollow_url = reverse('unfollow', args=['2'])
        self.follow_yourself_url = reverse('follow', args=['1'])
        self.show_followers_url = reverse('followers', args=['1'])
        self.show_following_url = reverse('following', args=['1'])

        DjGUser.objects.create_user(
            'test.email1@gmail.com',
            'username',
            'John',
            'strongpassword',
        )
        self.verified_user = DjGUser.objects.get(email='test.email1@gmail.com')
        self.verified_user.is_verified = True
        self.verified_user.save()
        self.verified_login_data = {
            'email': 'test.email1@gmail.com',
            'password': 'strongpassword'
        }

        DjGUser.objects.create_user(
            'test.email2@gmail.com',
            'username2',
            'Jane',
            'strongpassword',
        )
        self.verified_user2 = DjGUser.objects.get(email='test.email2@gmail.com')
        self.verified_user2.is_verified = True
        self.verified_user2.save()
        self.verified_login_data2 = {
            'email': 'test.email2@gmail.com',
            'password': 'strongpassword'
        }

        f = BytesIO()
        image = Image.new(mode='RGB', size=(100, 100))
        image.save(f, 'JPEG')
        f.seek(0)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg",
            content=f.read(),
        )

        self.profile_settings = {
            'username': 'username',
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'bio',
            'avatar': self.test_image
        }
        self.new_post = {
            'image': self.test_image,
            'tags': 'some tags'
        }

        self.client.post(self.login_url, self.verified_login_data)
        self.client.post(self.new_post_url, self.new_post)
        self.new_post2 = {
            'image': self.test_image,
            'tags': 'some tags2'
        }

        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_profile.html')

    def test_profile_GET_content_own_profile(self):
        response = self.client.get(self.profile_url)
        assert b'Update' in response.content

    def test_profile_settings_GET(self):
        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_settings.html')

    def test_profile_settings_POST(self):
        response = self.client.post(self.profile_settings_url, self.profile_settings)
        self.assertEqual(response.status_code, 200)

    def test_new_post_GET(self):
        response = self.client.get(self.new_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_post.html')

    def test_new_post_POST(self):
        response = self.client.post(self.new_post_url, self.new_post)
        self.assertEqual(response.status_code, 200)

    def test_delete_user_GET(self):
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_user.html')

    def test_delete_user_POST(self):
        response = self.client.post(self.delete_user_url)
        self.assertEqual(response.status_code, 302)

    def test_show_one_post_GET_correctly(self):
        response = self.client.get(self.one_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_one_post.html')

    def test_show_one_post_GET_post_dont_exist(self):
        response = self.client.get(self.post_dont_exist_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_GET_logged_in_deletes_own_post(self):
        response = self.client.get(self.delete_post_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_post_GET_logged_in_deletes_someones_post(self):
        self.client.post(self.logout_url)
        self.client.post(self.login_url, self.verified_login_data2)
        response = self.client.get(self.delete_post_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_post_POST(self):
        response = self.client.post(self.delete_post_url)
        self.assertEqual(response.status_code, 302)

    def test_like_post_GET(self):
        response = self.client.get(self.like_post_url)
        self.assertEqual(response.status_code, 302)

    def test_like_post_GET_more_than_once(self):
        self.client.get(self.like_post_url)
        response = self.client.get(self.like_post_url)
        self.assertEqual(response.status_code, 302)

    def test_unlike_post_GET(self):
        self.client.get(self.like_post_url)
        response = self.client.get(self.unlike_post_url)
        self.assertEqual(response.status_code, 302)

    def test_unlike_post_GET_more_than_once(self):
        self.client.get(self.unlike_post_url)
        response = self.client.get(self.unlike_post_url)
        self.assertEqual(response.status_code, 302)

    def test_show_likes_GET(self):
        response = self.client.get(self.show_likes_url)
        self.assertEqual(response.status_code, 200)

    def test_follow_GET(self):
        response = self.client.get(self.follow_url)
        self.assertEqual(response.status_code, 302)

    def test_follow_GET_yourself(self):
        response = self.client.get(self.follow_yourself_url)
        self.assertEqual(response.status_code, 302)

    def test_follow_GET_more_than_once(self):
        self.client.get(self.follow_url)
        response = self.client.get(self.follow_url)
        self.assertEqual(response.status_code, 302)

    def test_unfollow_GET(self):
        response = self.client.get(self.unfollow_url)
        self.assertEqual(response.status_code, 302)

    def test_unfollow_GET_more_than_once(self):
        self.client.get(self.unfollow_url)
        response = self.client.get(self.unfollow_url)
        self.assertEqual(response.status_code, 302)

    def test_show_followers_GET(self):
        response = self.client.get(self.show_followers_url)
        self.assertEqual(response.status_code, 200)

    def test_show_following_GET(self):
        response = self.client.get(self.show_following_url)
        self.assertEqual(response.status_code, 200)


class TestViewsNotLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.profile_url = reverse('profile')
        self.profile_settings_url = reverse('profile settings')
        self.new_post_url = reverse('new post')
        self.delete_user_url = reverse('delete user')
        self.one_post_url = reverse('show one post', args=['1'])
        self.delete_post_url = reverse('delete post', args=['1'])
        self.like_post_url = reverse('like', args=['1'])
        self.unlike_post_url = reverse('unlike', args=['1'])
        self.show_likes_url = reverse('show likes', args=['1'])
        self.follow_url = reverse('follow', args=['1'])
        self.unfollow_url = reverse('unfollow', args=['1'])
        self.show_followers_url = reverse('followers', args=['1'])
        self.show_following_url = reverse('following', args=['1'])

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

        DjGUser.objects.create_user(
            'test.email1@gmail.com',
            'username',
            'John',
            'strongpassword',
        )
        self.verified_user = DjGUser.objects.get(email='test.email1@gmail.com')
        self.verified_user.is_verified = True
        self.verified_user.save()
        self.verified_login_data = {
            'email': 'test.email1@gmail.com',
            'password': 'strongpassword'
        }
        self.client.post(self.login_url, self.verified_login_data)

        f = BytesIO()
        image = Image.new(mode='RGB', size=(100, 100))
        image.save(f, 'JPEG')
        f.seek(0)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg",
            content=f.read(),
        )

        self.new_post = {
            'image': self.test_image,
            'tags': 'some tags'
        }
        self.client.post(self.new_post_url, self.new_post)
        self.client.get(self.logout_url)

        return super().setUp()

    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_settings_GET(self):
        response = self.client.get(self.profile_settings_url)
        self.assertEqual(response.status_code, 302)

    def test_new_post_GET(self):
        response = self.client.get(self.new_post_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_user_GET(self):
        response = self.client.get(self.delete_user_url)
        self.assertEqual(response.status_code, 302)

    def test_like_post_GET(self):
        response = self.client.get(self.like_post_url)
        self.assertEqual(response.status_code, 302)

    def test_unlike_post_GET(self):
        self.client.get(self.like_post_url)
        response = self.client.get(self.unlike_post_url)
        self.assertEqual(response.status_code, 302)

    def test_show_likes_GET(self):
        response = self.client.get(self.show_likes_url)
        self.assertEqual(response.status_code, 302)

    def test_follow_GET(self):
        response = self.client.get(self.follow_url)
        self.assertEqual(response.status_code, 302)

    def test_unfollow_GET(self):
        response = self.client.get(self.unfollow_url)
        self.assertEqual(response.status_code, 302)

    def test_show_followers_GET(self):
        response = self.client.get(self.show_followers_url)
        self.assertEqual(response.status_code, 302)

    def test_show_following_GET(self):
        response = self.client.get(self.show_following_url)
        self.assertEqual(response.status_code, 302)
