from django.test import SimpleTestCase
from django.urls import reverse, resolve

from myapp.views import show_posts


class TestUrls(SimpleTestCase):

    def test_posts_url(self):
        url = reverse('home')
        print(url)
        print(resolve(url))
        self.assertEqual(resolve(url), show_posts)