from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .. import views


class TestUrls(SimpleTestCase):

    def test_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_user)

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.logout_user)

    def test_register(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_confirm_email(self):
        url = reverse('confirm email', args={'uidb64': 1, 'token': 1})
        self.assertEqual(resolve(url).func, views.confirm_email)

    def test_profile(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.show_profile)

    def test_profile_settings(self):
        url = reverse('profile settings')
        self.assertEqual(resolve(url).func, views.profile_settings)

    def test_new_post(self):
        url = reverse('new post')
        self.assertEqual(resolve(url).func, views.new_post)

    def test_delete_user(self):
        url = reverse('delete user')
        self.assertEqual(resolve(url).func, views.delete_user)

    def test_show_one_post(self):
        url = reverse('show one post', args=['1'])
        self.assertEqual(resolve(url).func, views.show_one_post)

    def test_delete_post(self):
        url = reverse('delete post', args=['1'])
        self.assertEqual(resolve(url).func, views.delete_post)

    def test_show_likes(self):
        url = reverse('show likes', args=['1'])
        self.assertEqual(resolve(url).func, views.show_likes)

    def test_like(self):
        url = reverse('like', args=['1'])
        self.assertEqual(resolve(url).func, views.like_post)

    def test_follow(self):
        url = reverse('follow', args=['1'])
        self.assertEqual(resolve(url).func, views.follow_user)

    def test_followers(self):
        url = reverse('followers', args=['1'])
        self.assertEqual(resolve(url).func, views.show_followers)

    def test_following(self):
        url = reverse('following', args=['1'])
        self.assertEqual(resolve(url).func, views.show_followings)