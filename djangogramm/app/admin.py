from django.contrib import admin

from .models import DjGUser, Image, Post

admin.site.register(DjGUser)
admin.site.register(Image)
admin.site.register(Post)
