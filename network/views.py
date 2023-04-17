from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post
from django.core.paginator import Paginator

def index(request):
    if request.method == 'POST':
        postText = request.POST.get('postText')
        form_type = request.POST.get('formType')
        if request.POST.get('post'):
            p_id = request.POST.get('post')
            post = Post.objects.get(pk=p_id)
            post.content = postText
            post.save()
        elif(request.POST.get('delete')):
            p_id = request.POST.get('delete')
            post = Post.objects.get(pk=p_id)
            post.delete()
        else:
            post = Post.objects.create(content=postText, author=request.user)

        post_list = Post.objects.all()
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'network/index.html', {'posts': posts})

    else:
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'network/index.html', {'posts': posts})

def profile(request, user_id):
    #if request.method == 'POST':
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(author=user)
        following_usernames = request.user.following.all().values_list('username', flat=True)
        print(following_usernames)
        return render(request, 'network/profile.html', {'posts':posts, 'username':user.username, 'followers_count':user.followers_count, 'following_count':user.following_count, 'following':following_usernames, 'author_id':user.id})
    

def follow(request, user_id):
    #if request.method == 'POST':
    user = User.objects.get(id=user_id)
    #following_usernames = request.user.following.all().values_list('username', flat=True)

    if request.user in user.followers.all():
        # User is already following, so unfollow
        user.followers.remove(request.user)
        user.followers_count -= 1
        request.user.following_count -= 1

    else:
        # User is not following, so follow
        user.followers.add(request.user)
        user.followers_count += 1
        request.user.following_count += 1                                                    

    user.save()
    request.user.save()
    following_usernames = request.user.following.all().values_list('username', flat=True)
    posts = Post.objects.filter(author=user)

    '''    user = User.objects.get(id=user_id)
        user.followers.add(request.user)
        posts = Post.objects.filter(author=user)        
        user.followers_count += 1
        user.save()
        request.user.following_count += 1
        request.user.save()
        following_usernames = request.user.following.all().values_list('username', flat=True)
        print(following_usernames)'''

    return render(request, 'network/profile.html', {'posts':posts, 'username':user.username, 'followers_count':user.followers_count, 'following_count':user.following_count, 'following':following_usernames, 'author_id':user.id})


def like_post(request, post_id):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=post_id)
            if post.liked_by.filter(id=request.user.id).exists():
                # User has already liked the post, so remove their like
                post.liked_by.remove(request.user)
                data = {'success': True, 'liked': False, 'likes': post.liked_by.count()}
            else:
                # User has not liked the post yet, so add their like
                post.liked_by.add(request.user)
                data = {'success': True, 'liked': True, 'likes': post.liked_by.count()}
            return JsonResponse(data)
        else:
            data = {'success': False, 'message': 'Please login to like a post'}
            return JsonResponse(data)

@login_required
def dislike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.dislikes -= 1
    post.save()
    messages.success(request, 'Post disliked successfully.')
    return redirect('index')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request, post_id=None):
    if post_id:
        post = Post.objects.get(pk=post_id)
        return render(request, 'network/newPost.html', {'post':post})
    return render(request, 'network/newPost.html')

def following(request):
    following_users = request.user.following.all()    
    posts = Post.objects.filter(author__in=following_users)
    return render(request, 'network/following.html', {'posts':posts})
