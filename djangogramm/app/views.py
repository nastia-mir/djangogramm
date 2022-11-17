from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import DjGUserSettingsForm, ImageFormAvatar, DjGUserCreationForm, PostForm, ImageForm
from .models import DjGUser, Post, Image
from .tokens import account_activation_token


def home(request):
    posts = Post.objects.prefetch_related('images').order_by('-time_created')
    context = {'posts': posts}
    return render(request, 'home.html', context)


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = DjGUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_verified:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'You need to confirm your email first.')
        else:
            messages.error(request, 'Wrong email or password.')

    return render(request, 'login.html')


def logout_user(request):
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


def register(request):
    form = DjGUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = DjGUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            activate_email(request, user)
        else:
            try:
                existing_user = DjGUser.objects.get(email=form.email)
            except:
                messages.error(request, 'This email is already used.')

    return render(request, 'register.html', context)


def confirm_email(request, uidb64, token):
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


@login_required(login_url='login')
def show_profile(request):
    uid = request.GET.get('uid', None)
    if not uid:
        followers = request.user.user_followers.all().count()
        followings = request.user.user_following.all().count()
        context = {'user': request.user,
                   'uid': None,
                   'followers': followers,
                   'followings': followings}
        return render(request, 'show_profile.html', context)
    else:
        try:
            user = DjGUser.objects.get(user_id=uid)
            followers = user.user_followers.all().count()
            followings = user.user_following.all().count()

            context = {'user': user,
                       'uid': uid,
                       'followers': followers,
                       'followings': followings
                       }
            return render(request, 'show_profile.html', context)
        except:
            return redirect('home')


@login_required(login_url='login')
def profile_settings(request):
    user_form = DjGUserSettingsForm(instance=request.user)
    avatar_form = ImageFormAvatar(instance=request.user.avatar)
    if request.method == 'POST':
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
    context = {'user_form': user_form,
               'avatar_form': avatar_form
    }
    return render(request, 'profile_settings.html', context)


@login_required(login_url='login')
def new_post(request):
    img_form = ImageForm()
    form = PostForm()
    if request.method == 'POST':
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

    context = {'form': form,
               'img_form': img_form}
    return render(request, 'new_post.html', context)


@login_required(login_url='login')
def delete_user(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    context = {'user': user}
    return render(request, 'delete_user.html', context)


def show_one_post(request, post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except:
        return redirect('home')
    images = post.images.all()
    likes = post.count_likes()
    context = {'post': post,
               'images': images,
               'likes': likes}
    return render(request, 'show_one_post.html', context)


@login_required(login_url='login')
def delete_post(request, post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except:
        return redirect('home')

    if request.user == post.user:
        if request.method == 'POST':
            post.delete()
            return redirect('home')
    else:
        return redirect('home')

    context = {'post': post}
    return render(request, 'delete_post.html', context)


@login_required(login_url='login')
def like_post(request, post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except:
        redirect('home')
    if post.likes.filter(user_id=request.user.user_id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('show one post', args=[post_id]))


@login_required(login_url='login')
def show_likes(request, post_id):
    try:
        post = Post.objects.get(post_id=post_id)
    except:
        redirect('home')

    users = post.likes.all()
    likes = post.count_likes()
    context = {'users': users,
               'likes': likes}
    return render(request, 'show_likes.html', context)


@login_required(login_url='login')
def follow_user(request, user_id):
    try:
        user = DjGUser.objects.get(user_id=user_id)
    except:
        redirect('home')

    print(request.user.followings)
    if request.user.followings.get(user):
        request.user.followings.remove(user)
        user.followers.remove(request.user)
    else:
        request.user.followings.add(user)
        user.followers.add(request.user)

    return HttpResponseRedirect("profile/?uid='{}'".format(user_id))


@login_required(login_url='login')
def show_followers(request, user_id):
    return render(request, 'followers.html')


@login_required(login_url='login')
def show_followings(request, user_id):
    return render(request, 'followings.html')
