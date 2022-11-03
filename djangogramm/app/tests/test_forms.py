from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from ..forms import DjGUserCreationForm, DjGUserSettingsForm, ImageForm, PostForm


class TestForms(TestCase):
    def setUp(self):
        f = BytesIO()
        image = Image.new(mode='RGB', size=(100, 100))
        image.save(f, 'JPEG')
        f.seek(0)
        self.test_image = SimpleUploadedFile(
            "test_image.jpg",
            content=f.read(),
        )
        return super().setUp()

    def test_djguser_creation_valid_data(self):
        form = DjGUserCreationForm(data={
            'email': 'testemail@gmail.com',
            'username': 'username',
            'first_name': 'John',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        })

        self.assertTrue(form.is_valid())

    def test_djguser_creation_no_data(self):
        form = DjGUserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_djguser_settings_valid_data(self):
        form = DjGUserSettingsForm(
            data={
                'username': 'username',
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'bio'},
            files={'avatar': self.test_image}
        )
        self.assertTrue(form.is_valid())

    def test_djguser_settings_no_data(self):
        form = DjGUserSettingsForm(data={}, files={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

