from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ImageField, ClearableFileInput
from .models import DjGUser, Post, Image


class DjGUserCreationForm(UserCreationForm):
    class Meta:
        model = DjGUser
        fields = ['email', 'username', 'first_name', 'password1', 'password2']


class ImageFormAvatar(ModelForm):
    image = ImageField(label='Avatar', widget=ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Image
        fields = ['image']


class DjGUserSettingsForm(ModelForm):
    class Meta:
        model = DjGUser
        fields = ['username', 'first_name', 'last_name', 'bio']


class ImageForm(ModelForm):
    image = ImageField(label='images', widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['image']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['tags']
