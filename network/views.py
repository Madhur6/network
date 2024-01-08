import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Post, Comment, UserProfile, Following

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import User

from django.utils.translation import gettext_lazy as _

from .forms import CreatePostForm, CreateCommentForm, CreateUserProfileForm

from itertools import chain

from django.conf import settings


def index(request):
    posts = Post.objects.order_by("-date").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')

    try: 
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        #if the page number is not an Integer, Set it to the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        #If the page number is out of range, Set it to the last page
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, "network/index.html", {
        "post_form": CreatePostForm(),
        "comment_form": CreateCommentForm(auto_id=False),
        "page_obj": page_obj,
        "add_post": True
    })


@login_required(login_url="network:login")
def new_post_comment(request, action):
    if request.method == "GET":
        return HttpResponse(status=405)
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()

    if request.method == "POST":
        if action=="post":
            form = CreatePostForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]

                post = Post(
                    user = User.objects.get(pk=request.user.id),
                    content = content
                )
                post.save()
        
        elif action == "comment":
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]

                # Get commented post
                try:
                    post = Post.objects.get(pk=request.POST.get('postId'))
                except Post.DoesNotExist:
                    return HttpResponse(status=404)
                
                comment = Comment(
                    user = User.objects.get(pk=request.user.id),
                    content = content,
                    post = post
                )
                comment.save()
        
        #Redirect the user back to place from where the request came
        return HttpResponseRedirect(request.headers['Referer'])
    
    if request.method == "PUT":
        body = json.loads(request.body)
        try:
            if action == "post":
                ObjectPUT = Post.objects.get(pk=body.get('id'), user=request.user)
            else:
                ObjectPUT = Comment.objects.get(pk=body.get('id'), user=request.user)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return JsonResponse({
                "error": _("Post or Comment does not exists!")
            }, status=404)
        
        ObjectPUT.content = body.get('content')
        ObjectPUT.save()

        return HttpResponse(status=201)
    
    if request.method == "DELETE":
        body = json.loads(request.body)
        try:
            if action == "post":
                ObjectDelete = Post.objects.get(pk=body.get('id'), user=request.user)
            else:
                ObjectDelete = Comment.objects.get(pk=body.get('id'), user=request.user)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return JsonResponse({
                "error": _("Post or Comment does not exists!")
            }, status=404)
        
        ObjectDelete.delete()
        return HttpResponse(status=204)



@login_required(login_url="network:login")
def user_profile(request, user_id):
    user_data = User.objects.get(pk=user_id)
    posts = user_data.posts.order_by("-date").all()
    # print(posts)

    # filter(user=user_id), Relationships where the current user is the one following
    following_list = Following.objects.filter(user=user_id).values_list('user_followed', flat=True)
    
    # filter(user_followed=user_id), Relationships where the current user is the one being followed
    followers_list = Following.objects.filter(user_followed=user_id).values_list('user', flat=True)

    #All the users that the current user is following
    following_user = User.objects.filter(id__in=following_list)

    #All the users following the current user
    followers_user = User.objects.filter(id__in=followers_list)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')

    try: 
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        #if the page number is not an Integer, Set it to the first page
        page_obj = paginator.get_page(1)
    except EmptyPage:
        #If the page number is out of range, Set it to the last page
        page_obj = paginator.get_page(paginator.num_pages)

    return render(request, "network/user_profile.html", {
        "user_obj": user_data,
        "following": following_user,
        "followers": followers_user,
        "page_obj": page_obj,
        "comment_form": CreateCommentForm(auto_id=False)
    })




@login_required(login_url="network:login")
def following(request):
    current_user = User.objects.get(pk=request.user.id)

    posts = [users.followed_user_posts() for users in current_user.following.all()]

    posts = list(chain(*posts))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "post_form": None,
        "comment_form": CreateCommentForm(auto_id=False),
        "page_obj": page_obj,
        "add_post": False
    })



@login_required(login_url="network:login")
def follow_unfollow(request, user_id):
    if request.method == "GET":
        return HttpResponse(status=405)
    
    if request.method == "POST":
        try:
            following_obj = Following.objects.get(user=request.user.id, user_followed=user_id)
        except Following.DoesNotExist:
            try:
                follow_user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return HttpResponse(status=404)
            else:
                new_follow_obj = Following(user=request.user, user_followed=follow_user)
                new_follow_obj.save()
        else:
            following_obj.delete()

        return HttpResponseRedirect(reverse("network:user_profile", args=[user_id,]))

 

@login_required(login_url="network:login")
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == "POST":
        #cancel the edit request
        if request.POST.get("cancel") == "clicked":
            return HttpResponseRedirect(reverse("network:user_profile", args=[request.user.id]))
        
        #Edit the profile
        form = CreateUserProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            #update all profile's data with form's data
            user_profile.name = form.cleaned_data.get("name")
            user_profile.date_of_birth = form.cleaned_data.get("date_of_birth")
            user_profile.about = form.cleaned_data.get("about")
            user_profile.country = form.cleaned_data.get("country")

            #update image only if the file was uploaded
            if len(request.FILES) == 1:
                user_profile.image = request.FILES['image']
            
            user_profile.save()

            return HttpResponseRedirect(reverse("network:user_profile", args=[request.user.id]))
        else:
            return render(request, "network/edit_profile.html", {
                "form": form,
                "max_file_size": settings.MAX_UPLOAD_SIZE
            })
    
    return render(request, "network/edit_profile.html", {
        "form": CreateUserProfileForm(instance=request.user.profile),
        "max_file_size": settings.MAX_UPLOAD_SIZE
    })


@login_required(login_url="network:login")
def like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user = request.user

        if request.method == "GET":
            is_liked = post.liked_by.filter(id=user.id).exists()
            data = {
                'id': post.id,
                'liked': is_liked,
                'likes': post.liked_by.count(),
            }
            return JsonResponse(data)
        
        elif request.method == 'PUT':
            is_liked = post.liked_by.filter(id=user.id).exists()
            if is_liked:
                post.liked_by.remove(user)
            else:
                post.liked_by.add(user)
            data = {
                'id': post.id,
                # client-side JavaScript doesn't directly change the server's database. It sends a request to the server, and then the server changes its own database.
                'liked': not is_liked, #toggled to its opposite state
                'likes': post.liked_by.count(),
            }
            return JsonResponse(data)
        
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found!'}, status=404)




@login_required(login_url="network:login")
def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        user = request.user

        if request.method == "GET":
            is_liked = comment.liked_by.filter(id=user.id).exists()
            data = {
                'id': comment.id,
                'liked': is_liked,
                'likes': comment.liked_by.count(),
            }
            return JsonResponse(data)
        
        elif request.method == "PUT":
            is_liked = comment.liked_by.filter(id=user.id).exists()
            if is_liked:
                comment.liked_by.remove(user)
            else:
                comment.liked_by.add(user)
            data = {
                'id': comment.id,
                'liked': not is_liked,
                'likes': comment.liked_by.count(),
            }
            return JsonResponse(data)
    
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found!'}, status=404)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            #redirect user to the page he/she were trying to access before they got redirected to the login page('@login_required')
            if "next" in request.POST:
                request_args = request.POST.get("next")[1:].split('/')
                return HttpResponseRedirect(reverse("network" + request_args[0], args=request_args[1:]))
            else:
                return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
        
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


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
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
