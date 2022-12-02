from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from taggit.managers import TaggableManager


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', max_length=100)

    objects = models.Manager()

    def __str__(self):
        return "Image {}".format(self.image_id)


class DjGUserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_verified', True)
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
    avatar = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

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
    likes = models.ManyToManyField(DjGUser, related_name='post_likes')

    objects = models.Manager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'time_created'], name='unique_post')]

    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return "Post id:{}, user:{}".format(self.post_id, self.user)


class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    follow_from = models.ForeignKey(DjGUser, related_name='follow_to', on_delete=models.CASCADE)
    follow_to = models.ForeignKey(DjGUser, related_name='follow_from', on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return "{} follows {}".format(self.follow_from, self.follow_to)