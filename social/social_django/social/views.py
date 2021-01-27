from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def feed(req):
    posts = Post.objects.all()
    ctx = {'posts': posts}

    return render(req, 'social/feed.html', ctx)

def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(req, f'Usuario {username} ha sido creado')
            return redirect('feed')
    else:
        form = UserRegisterForm()

    ctx = { 'form': form }

    return render(req, 'social/register.html', ctx)

@login_required

def post(req):
    current_user = get_object_or_404(User, pk=req.user.pk)
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(req, 'Post enviado')
            return redirect('feed')

    else:
        form = PostForm()

    ctx = {'form': form}
    
    return render(req, 'social/post.html', ctx)



def profile(req, username=None):
    current_user = req.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(req, 'social/profile.html', {'user': user, 'posts':posts})


def follow(req, username):
    current_user = req.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user= to_user_id)
    rel.save()
    messages.success(req, f'Sigues a {username}')
    return redirect('feed')

def unfollow(req, username):
    current_user = req.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(req, f'Dejaste de seguir a {username}')
    return redirect('feed')