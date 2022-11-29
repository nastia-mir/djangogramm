from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('confirm/<uidb64>/<token>', views.confirm_email, name='confirm email'),

    path('profile/', views.show_profile, name='profile'),
    path('profile/settings', views.profile_settings, name='profile settings'),
    path('profile/newpost', views.new_post, name='new post'),
    path('profile/deleteuser', views.delete_user, name='delete user'),

    path('post/<post_id>', views.show_one_post, name='show one post'),
    path('post/<post_id>/deletepost', views.delete_post, name='delete post'),

    path('post/<post_id>/users_liked', views.show_likes, name='show likes'),
    path('post/<post_id>/like', views.like_post, name='like'),
    path('post/<post_id>/unlike', views.unlike_post, name='unlike'),

    path('follow/<user_id>', views.follow_user, name='follow'),
    path('unfollow/<user_id>', views.unfollow_user, name='unfollow'),
    path('followers/<user_id>', views.show_followers, name='followers'),
    path('followings/<user_id>', views.show_followings, name='following')
    ]
