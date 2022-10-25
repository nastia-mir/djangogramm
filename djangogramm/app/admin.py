from django.contrib import admin

from .models import DjGUser, Image, Post, Like

admin.site.register(DjGUser)
admin.site.register(Image)
admin.site.register(Post)
admin.site.register(Like)
