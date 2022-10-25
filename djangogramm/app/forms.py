from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ImageField, ClearableFileInput

from .models import DjGUser, Post, Image


class DjGUserSettingsForm(ModelForm):
    class Meta:
        model = DjGUser
        fields = ['username', 'first_name', 'last_name', 'bio', 'avatar']


class DjGUserCreationForm(UserCreationForm):
    class Meta:
        model = DjGUser
        fields = ['email', 'username', 'first_name', 'password1', 'password2']


class ImageForm(ModelForm):
    image = ImageField(label='images', widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['image']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['tags']
