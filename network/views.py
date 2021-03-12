from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Follow

class newPostForm(forms.Form):
    content = forms.CharField(label="What's on your mind right now?", widget=forms.Textarea(attrs={
    'style' : 'width:100%', 'class': 'form-control'}))

def index(request):
    return HttpResponseRedirect(reverse('all'))


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

@login_required(login_url='/login')
def new(request):
    if request.method == "POST":
        form = newPostForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            p = Post(user=request.user, content=content)
            p.save()
            return HttpResponseRedirect(reverse("all"))
        
        return render(request, "network/new.html", {
            "form": form
        })       
    
    else:
        return render(request, "network/new.html", {
            "form": newPostForm()
        })

def all(request):
    paginator = Paginator(Post.objects.all().order_by('id').reverse(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/all.html", {
        "posts": page_obj
    })

@login_required(login_url='/login')
def profile(request, user):
    followed = False
    if (request.user.id != user):
        # if the person on this page has at least one follower
        if (Follow.objects.filter(follower=user)):
            # if the user using the app has already followed the person on this page
            try:
                Follow.objects.get(follower=User.objects.get(id=request.user.id), following=User.objects.get(id=user))
                followed = True
            # the user using the app has not followed the person on this page
            except Follow.DoesNotExist:
                followed = False
        # user of this page has no followers
        else:
            followed = False
    
    return render(request, "network/profile.html", {
        "profile_user": User.objects.get(pk=user),
        "followed": followed,
        "posts": Post.objects.filter(user=user).order_by('id').reverse(),
        "following": Follow.objects.filter(follower=user).count(),
        "follower": Follow.objects.filter(following=user).count()
    })


def following(request):
    following = Follow.objects.filter(follower=request.user).values('following_id')

    posts = Post.objects.filter(user__in=following).order_by('id')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj
    })

@csrf_exempt
def edit(request):
    try:
        post_id = int(request.POST.get("post_id"))
    except:
        return HttpResponse("The post doesn't exist")
        
    post = Post.objects.get(id=post_id)
    post.content = request.POST.get("content")

    post.save(update_fields=["content"])

    return HttpResponse("You've successfully edited the post")

@login_required(login_url='/login')
def follow(request, user):
    # Unfollow
    if (User.objects.get(id=request.user.id) != User.objects.get(id=user)):
        try: 
            f = Follow.objects.get(follower=User.objects.get(id=request.user.id), following=User.objects.get(id=user))
            f.delete()
            return HttpResponse("Unfollowed")
        
        # Follow
        except Follow.DoesNotExist:
            f = Follow(follower=User.objects.get(id=request.user.id), following=User.objects.get(id=user))
            f.save()
            return HttpResponse("Followed")
    return HttpResponse("You can't follow yourself")

@login_required(login_url='/login')
def like(request, post_id):
    try:
        liked = User.objects.get(pk=request.user.id).lposts
        post = Post.objects.get(pk=post_id)
    except:
        return HttpResponse("You don't have access to this function")
    # Unlike a post if the post has been liked
    if post in liked.all():
        liked.remove(post)
    # Like the post
    else:
        liked.add(post)

    return HttpResponse("You've successfully liked/unliked a post")
