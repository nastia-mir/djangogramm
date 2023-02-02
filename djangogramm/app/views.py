from random import sample

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.db.models import Q

from app.forms import DjGUserSettingsForm, ImageFormAvatar, DjGUserCreationForm, PostForm, ImageForm
from app.models import DjGUser, Post, Image, Follower
from app.tokens import account_activation_token


@require_http_methods(["GET"])
@login_required(login_url='login')
def home(request):
    if request.method == "GET":
        followings = Follower.objects.filter(follow_from=request.user)

        posts = Post.objects.filter(Q(user=request.user) | Q(user__in=followings.values('follow_to'))). \
            prefetch_related('images').order_by('-time_created')
        not_followed = list(DjGUser.objects.exclude(Q(username=request.user.username) |
                                                    Q(username__in=followings.values('follow_to__username'))))
        if len(not_followed) < 5:
            context = {'posts': posts,
                       'not_followed': not_followed}
        else:
            random_not_followed = sample(not_followed, 5)
            context = {'posts': posts,
                       'not_followed': random_not_followed}
        return render(request, 'home.html', context)


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = DjGUser.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        except:
            messages.error(request, 'User does not exist.')

        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'You need to confirm your email first.')
                return redirect('login')
        else:
            messages.error(request, 'Wrong email or password.')
            return redirect('login')

    elif request.method == 'GET':
        return render(request, 'login.html')


@require_http_methods(["GET"])
def logout_user(request):
    if request.method == "GET":
        logout(request)
        return redirect('home')


def activate_email(request, user):
    subject = 'Email confirmation'
    message = render_to_string("email.html", {
        'user': user,
        'domain': get_current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.user_id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    if email:
        messages.success(request, 'We send you a email to complete the registration.')
    else:
        messages.error(request, "We couldn't send you an email, please check if you typed it correctly.")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = DjGUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            activate_email(request, user)
            return redirect('login')
        else:
            try:
                existing_user = DjGUser.objects.get(email=form.email)
            except:
                messages.error(request, 'This email is already used.')
                return redirect('register')

    elif request.method == "GET":
        form = DjGUserCreationForm()
        context = {'form': form}

        return render(request, 'register.html', context)


@require_http_methods(["GET"])
def confirm_email(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = DjGUser.objects.get(user_id=uid)
        except:
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_verified = True
            user.save()

        context = {'user': user}
        return render(request, 'confirm_email.html', context)


@require_http_methods(["GET"])
@login_required(login_url='login')
def show_profile(request):
    if request.method == "GET":
        uid = request.GET.get('uid', None)
        if not uid:
            followers = Follower.objects.filter(follow_to=request.user).count()
            following = Follower.objects.filter(follow_from=request.user).count()
            user = request.user
            active_user_follows = False
        else:
            try:
                user = DjGUser.objects.get(user_id=uid)
                followers = Follower.objects.filter(follow_to=user).count()
                following = Follower.objects.filter(follow_from=user).count()

                if request.user == user:
                    uid = None

                if Follower.objects.filter(follow_from=request.user, follow_to=user):
                    active_user_follows = True
                else:
                    active_user_follows = False

            except:
                return redirect('home')

        context = {'user': user,
                   'uid': uid,
                   'followers': followers,
                   'followings': following,
                   'active_user_follows': active_user_follows}
        return render(request, 'show_profile.html', context)


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def profile_settings(request):
    if request.method == "GET":
        user_form = DjGUserSettingsForm(instance=request.user)
        avatar_form = ImageFormAvatar(instance=request.user.avatar)
        context = {'user_form': user_form,
                   'avatar_form': avatar_form
                   }
        return render(request, 'profile_settings.html', context)
    elif request.method == 'POST':
        user_form = DjGUserSettingsForm(request.POST, instance=request.user)
        avatar_form = ImageFormAvatar(request.POST, request.FILES, instance=request.user.avatar)
        if user_form.is_valid() and avatar_form.is_valid():
            user_form.save(commit=False)
            avatar = request.FILES.get('image')
            if avatar:
                image = Image(image=avatar)
                image.save()
                request.user.avatar = image
                user_form.save()
            else:
                user_form.save()
            return redirect("profile")
        else:
            messages.error(request, 'Something went wrong.')
            return redirect('profile settings')


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def new_post(request):
    if request.method == 'GET':
        img_form = ImageForm()
        form = PostForm()
        context = {'form': form,
                   'img_form': img_form}
        return render(request, 'new_post.html', context)
    elif request.method == 'POST':
        form = PostForm(request.POST)
        img_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid() and img_form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            imgs = []
            for img in images:
                image = Image(image=img, post=post)
                image.save()
                imgs.append(image)
            post.images.set(imgs)
            form.save_m2m()
            return redirect("/post/{}".format(post.post_id))


@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def delete_user(request):
    if request.method == 'GET':
        user = request.user
        context = {'user': user}
        return render(request, 'delete_user.html', context)
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')


@require_http_methods(["GET"])
@login_required(login_url='login')
def show_one_post(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(post_id=post_id)
            images = post.images.all()
            likes = post.count_likes()

            if request.user in post.likes.all():
                post_liked = True
            else:
                post_liked = False

            context = {'post': post,
                       'images': images,
                       'likes': likes,
                       'post_liked': post_liked}
            return render(request, 'show_one_post.html', context)
        except:
            return redirect('home')


@require_http_methods(["GET", "POST", "DELETE"])
@login_required(login_url='login')
def delete_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(post_id=post_id)
            if request.user == post.user:
                post.delete()
            return redirect('home')
        except:
            return redirect('home')

    elif request.method == 'GET':
        try:
            post = Post.objects.get(post_id=post_id)
            context = {'post': post}
            return render(request, 'delete_post.html', context)
        except:
            return redirect('home')


@require_http_methods(["POST"])
@login_required(login_url='login')
def like_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(post_id=post_id)
            if not post.likes.filter(user_id=request.user.user_id).exists():
                post.likes.add(request.user)
            return HttpResponseRedirect(reverse('show one post', args=[post_id]))
        except:
            redirect('home')


@require_http_methods(["POST"])
@login_required(login_url='login')
def unlike_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(post_id=post_id)
            if post.likes.filter(user_id=request.user.user_id).exists():
                post.likes.remove(request.user)
            return HttpResponseRedirect(reverse('show one post', args=[post_id]))
        except:
            redirect('home')


@require_http_methods(["GET"])
@login_required(login_url='login')
def show_likes(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(post_id=post_id)
            users = post.likes.all()
            likes = post.count_likes()
            context = {'users': users,
                       'likes': likes}
            return render(request, 'show_likes.html', context)
        except:
            redirect('home')


@require_http_methods(["POST"])
@login_required(login_url='login')
def follow_user(request, user_id):
    if request.method == 'POST':
        try:
            user = DjGUser.objects.get(user_id=user_id)
            if request.user == user:
                messages.error(request, 'You can not follow yourself.')

            elif not Follower.objects.filter(follow_from=request.user, follow_to=user):
                following = Follower.objects.create(follow_from=request.user, follow_to=user)
                following.save()

            return HttpResponseRedirect("/profile/?uid={}".format(user_id))
        except:
            redirect('home')


@require_http_methods(["POST"])
@login_required(login_url='login')
def unfollow_user(request, user_id):
    if request.method == 'POST':
        try:
            user = DjGUser.objects.get(user_id=user_id)
            if user == request.user:
                messages.error(request, 'You can not unfollow yourself.')

            try:
                following = Follower.objects.filter(follow_from=request.user, follow_to=user)
                if following:
                    Follower.objects.filter(follow_from=request.user, follow_to=user).delete()
                return HttpResponseRedirect("/profile/?uid={}".format(user_id))
            except:
                return HttpResponseRedirect("/profile/?uid={}".format(user_id))
        except:
            redirect('home')


@require_http_methods(["GET"])
@login_required(login_url='login')
def show_followers(request, user_id):
    if request.method == 'GET':
        try:
            user = DjGUser.objects.get(user_id=user_id)
            followers = Follower.objects.filter(follow_to=user).values('follow_from__username', 'follow_from__user_id')
            followers_count = len(followers)
            context = {'followers': followers,
                       'followers_count': followers_count,
                       'user': user}
            return render(request, 'followers.html', context)
        except:
            redirect('home')


@require_http_methods(["GET"])
@login_required(login_url='login')
def show_followings(request, user_id):
    if request.method == 'GET':
        try:
            user = DjGUser.objects.get(user_id=user_id)
            following = Follower.objects.filter(follow_from=user).values('follow_to__username', 'follow_to__user_id')
            following_count = len(following)
            context = {'following': following,
                       'followers_count': following_count,
                       'user': user}
            return render(request, 'followings.html', context)
        except:
            redirect('home')
