from django.urls import path

from . import views

urlpatterns = [

    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('register/confirm', views.confirm_email, name='confirm email'),

    path('profile/', views.show_profile, name='profile'),
    path('profile/settings', views.profile_settings, name='profile settings'),
    path('profile/newpost', views.new_post, name='new post'),
    path('profile/deleteuser', views.delete_user, name='delete user'),

    path('', views.show_posts, name='home'),
    path('post/<post_id>', views.show_one_post, name='show one post'),
    path('post/<post_id>/likes', views.show_likes, name='show likes'),
    path('post/<post_id>/deletepost', views.delete_post, name='delete post')
    ]