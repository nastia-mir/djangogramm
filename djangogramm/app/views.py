from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DjGUserSettingsForm, ImageFormAvatar, DjGUserCreationForm, PostForm, ImageForm
from .models import DjGUser, Post, Image


def home(request):
    posts = Post.objects.prefetch_related('image_set').order_by('-time_created')
    print(posts)
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
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Wrong email or password.')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    form = DjGUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = DjGUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('profile')
        else:
            try:
                existing_user = DjGUser.objects.get(email=form.email)
            except:
                messages.error(request, 'This email is already used.')

    return render(request, 'register.html', context)


def confirm_email(request):
    # not done
    return render(request, 'confirm_email.html')


def show_profile(request):
    uid = request.GET.get('uid', None)
    if not uid:
        avatar = Image.objects.filter(user=request.user.user_id).last()
        context = {'user': request.user,
                   'avatar': avatar}
        return render(request, 'show_profile.html', context)
    else:
        try:
            user = DjGUser.objects.get(user_id=uid)
            avatar = Image.objects.filter(user=uid).last()
            context = {'user': user,
                       'avatar': avatar}
            return render(request, 'show_profile.html', context)
        except:
            return redirect('home')


@login_required(login_url='login')
def profile_settings(request):
    avatar = Image.objects.filter(user=request.user.user_id).last()
    user_form = DjGUserSettingsForm(instance=request.user)
    avatar_form = ImageFormAvatar(instance=avatar)
    if request.method == 'POST':
        user_form = DjGUserSettingsForm(request.POST, instance=request.user)
        avatar_form = ImageFormAvatar(request.POST, request.FILES, instance=avatar)
        if user_form.is_valid() and avatar_form.is_valid():
            user_form.save()
            avatar = request.FILES.get('image')
            if avatar:
                image = Image(image=avatar, user=request.user)
                image.save()
            return redirect("profile")
        else:
            messages.error(request, 'Something went wrong.')
    context = {'user_form': user_form,
               'avatar_form': avatar_form}
    return render(request, 'profile_settings.html', context)


@login_required(login_url='login')
def new_post(request):
    img_form = ImageForm()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        img_form = ImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            for img in images:
                image = Image(image=img, post=post)
                image.save()
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
    images = Image.objects.filter(post=post_id)
    context = {'post': post,
               'images': images}
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


def show_likes(request):
    # not done
    return render(request, 'show_likes.html')
