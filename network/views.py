import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import New_Post, UserProfile
from .forms import NewPostForm
from .util import paginate_posts


@login_required
def index(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect('network:new_post') 
    else:
        form = NewPostForm()

    return render(request, "network/index.html", {'form': form})

@login_required
def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('network:new_post') 
        else:
            posts = New_Post.objects.all().order_by('-timestamp')
            page_obj = paginate_posts(request, posts)
    
            context = {
                'page_obj': page_obj
            }
            context['form'] = form
            context['posts'] = posts
            return render(request, "network/new_post.html", context)
                
    elif request.method == "GET":
        form = NewPostForm()
        posts = New_Post.objects.all().order_by('-timestamp')
        page_obj = paginate_posts(request, posts)

        context = {
        'form': form,
        'posts': posts,
        'page_obj': page_obj
        }
        return render(request, "network/new_post.html", context)

def profile(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    posts = New_Post.objects.filter(user=user).order_by('-timestamp')
    page_obj = paginate_posts(request, posts)
    
    is_following = False
    if request.user.is_authenticated:
        # Ensure a UserProfile exists for the logged-in user
        logged_in_user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        is_following = logged_in_user_profile.following.filter(id=user_profile.id).exists()

    context = {
        'profile_user': user,
        'is_following': is_following,
        'followers_count': user_profile.followers.count(),
        'following_count': user_profile.following.count(),
        'page_obj': page_obj
    }
    return render(request, 'network/profile.html', context)

@login_required
def following_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    followed_users = user_profile.following.all()
    posts = New_Post.objects.filter(user__in=followed_users).order_by('-timestamp')
    page_obj = paginate_posts(request, posts)

    return render(request, "network/following.html", {
        'page_obj': page_obj
    })
    
@csrf_exempt
@login_required
def update_post(request, post_id):
    post = get_object_or_404(New_Post, id=post_id)
    
    if post.user != request.user:
        return JsonResponse({"success": False, "error": "Not authorized."}, status=403)

    data = json.loads(request.body)
    post.content = data['content']
    post.save()
    return JsonResponse({"success": True})

def like_post(request, post_id):
    post = get_object_or_404(New_Post, id=post_id)
    user = request.user
    
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        
    return JsonResponse({"likes": post.likes.count()}, status=200)


def follow_unfollow(request, username):
    
    if request.method == "POST":
        # Get the target user and their profile
        target_user = get_object_or_404(get_user_model(), username=username)
        target_user_profile = UserProfile.objects.get(user=target_user)
        
        # Get the UserProfile for the current user
        current_user_profile = UserProfile.objects.get(user=request.user)

        if current_user_profile.following.filter(id=target_user.id).exists():
            current_user_profile.following.remove(target_user)
            target_user_profile.followers.remove(request.user)
            current_user_profile.save()
            status = "unfollowed"
        else:
            current_user_profile.following.add(target_user)
            target_user_profile.followers.add(request.user)
            current_user_profile.save()
            status = "followed"
            
        followers_count = target_user_profile.followers.count()
        following_count = target_user_profile.following.count()

        return JsonResponse({
            "status": status,
            "followers_count": followers_count,
            "following_count": following_count
        })

    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    
