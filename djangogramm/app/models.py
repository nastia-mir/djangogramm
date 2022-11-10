from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from taggit.managers import TaggableManager


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', max_length=100)

    objects = models.Manager()

    def __str__(self):
        return "Image '{}'".format(self.image_id)


class DjGUserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):
        values = {'email': email, 'username': username, 'first_name': first_name, 'password': password}
        for value in values:
            if not values[value]:
                raise ValueError("You must provide a '{}'.".format(value))

        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class DjGUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']
    objects = DjGUserManager()

    def __str__(self):
        return self.username


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DjGUser, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    tags = TaggableManager()
    time_created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return "Post id:'{}', user:'{}'".format(self.post_id, self.user)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    users = models.ManyToManyField(DjGUser)

    objects = models.Manager()

    def __str__(self):
        return "Like post='{}', users='{}'".format(self.post, self.users)


