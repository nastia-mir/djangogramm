from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ImageField, ClearableFileInput, TextInput, Textarea
from .models import DjGUser, Post, Image


class DjGUserCreationForm(UserCreationForm):
    class Meta:
        model = DjGUser
        fields = ['email', 'username', 'first_name', 'password1', 'password2']

        widgets = {
            'email': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'password1': TextInput(attrs={'class': 'form-control'}),
            'password2': TextInput(attrs={'class': 'form-control'})
        }


class ImageFormAvatar(ModelForm):
    image = ImageField(label='Avatar', widget=ClearableFileInput(attrs={'multiple': False}))

    class Meta:
        model = Image
        fields = ['image']


class DjGUserSettingsForm(ModelForm):
    class Meta:
        model = DjGUser
        fields = ['username', 'first_name', 'last_name', 'bio']

        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'bio': Textarea(attrs={'class': 'form-control'})
        }


class ImageForm(ModelForm):
    image = ImageField(label='Images', widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['image']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['tags']

        widgets = {'tags': TextInput(attrs={'class': 'form-control'})}
