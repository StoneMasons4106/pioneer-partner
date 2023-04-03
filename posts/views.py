from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Comment
from notifications.models import Notification
from profiles.models import UserProfile
from django.contrib.auth.models import User
import urllib
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

@login_required
def add_like(request):

    if request.method == "POST":
        post_id = request.body.decode()
        id = post_id.split('postId=')[1]
        post = get_object_or_404(Post, post_id=id)
        post.likes.add(request.user)
        post.save()

        post_user_profile = get_object_or_404(UserProfile, user=post.user)
        if post_user_profile.liked_post_notifications:
            hostname = os.environ.get('MY_HOSTNAME')
            new_notification = Notification(user=post.user, info=f'{request.user} liked your post.', url=f'{hostname}posts/{post.post_id}', status='1', type='2')
            new_notification.save()

            post_notification_message = render_to_string(
            'posts/emails/notification.txt', {
                'name': post.user,
                'my_hostname': os.environ.get('MY_HOSTNAME'),
                'notification_url': new_notification.url,
                'notification_type': new_notification.get_type_display()
                }
            )

            post_notification_message_wrapper = EmailMessage(
                f'New Notification: {new_notification.get_type_display()}',
                post_notification_message,
                to=[post.user.email]
            )

            post_notification_message_wrapper.send()

    return HttpResponse("OK")


@login_required
def remove_like(request):
    
    if request.method == "POST":
        post_id = request.body.decode()
        id = post_id.split('postId=')[1]
        post = get_object_or_404(Post, post_id=id)
        post.likes.remove(request.user)
        post.save()

    return HttpResponse("OK")


@login_required
def add_bookmark(request):

    if request.method == "POST":
        post_id = request.body.decode()
        id = post_id.split('postId=')[1]
        post = get_object_or_404(Post, post_id=id)
        post.bookmarks.add(request.user)
        post.save()

    return HttpResponse("OK")


@login_required
def remove_bookmark(request):

    if request.method == "POST":
        post_id = request.body.decode()
        id = post_id.split('postId=')[1]
        post = get_object_or_404(Post, post_id=id)
        post.bookmarks.remove(request.user)
        post.save()

    return HttpResponse("OK")


@login_required
def add_comment(request):

    if request.method == "POST":
        comment_info = request.body.decode('ascii', 'replace')
        original_post_id = comment_info.split('original-post-id=')[1].split('&comment-text')[0]
        comment_text = urllib.parse.unquote(comment_info.split('&comment-text=')[1], encoding='utf-8', errors='replace').replace("+", " ")
        original_post = Post.objects.filter(post_id=original_post_id)[0]
        profile = get_object_or_404(UserProfile, user=request.user)
        comment = Comment(original_post=original_post, congregation=profile.congregation, text_input=comment_text, user=request.user)
        comment.save()

        post_user_profile = get_object_or_404(UserProfile, user=original_post.user)
        if post_user_profile.comment_post_notifications:
            hostname = os.environ.get('MY_HOSTNAME')
            new_notification = Notification(user=original_post.user, info=f'{request.user} commented on your post.', url=f'{hostname}posts/{original_post.post_id}', status='1', type='3')
            new_notification.save()

            comment_notification_message = render_to_string(
            'posts/emails/notification.txt', {
                'name': post.user,
                'my_hostname': os.environ.get('MY_HOSTNAME'),
                'notification_url': new_notification.url,
                'notification_type': new_notification.get_type_display()
                }
            )

            comment_notification_message_wrapper = EmailMessage(
                f'New Notification: {new_notification.get_type_display()}',
                comment_notification_message,
                to=[post.user.email]
            )

            comment_notification_message_wrapper.send()

        messages.success(request, 'Your comment has been added.')
    
    return redirect(request.META['HTTP_REFERER'])


@login_required
def post(request, post_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    post = get_object_or_404(Post, post_id=post_id)
    user = get_object_or_404(User, username=request.user)
    comments = Comment.objects.filter(original_post=post.id)

    context = {
        'profile': profile,
        'post': post,
        'user': user,
        'comments': comments,
        'title': f'Pioneer Partner - Post From {post.user.username}',
    }

    return render(request, 'posts/post.html', context)


@login_required
def add_post(request):

    user = get_object_or_404(User, username=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        post = Post(user=user, congregation=profile.congregation, text_input=request.POST['post-text'])
        post.save()
        messages.success(request, 'Post successfully created.')

        return redirect('post', post_id=post.post_id)

    context = {
        'profile': profile,
        'user': user,
        'title': 'Pioneer Partner - Add Post',
    }

    return render(request, 'posts/add_post.html', context)


@login_required
def edit_post(request, post_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    post = get_object_or_404(Post, post_id=post_id)
    user = get_object_or_404(User, username=request.user)

    if request.method == "POST":
        post.text_input = request.POST['post-text']
        post.save()
        messages.success(request, 'Post successfully edited.')
        return redirect('post', post_id=post.post_id)

    context = {
        'profile': profile,
        'post': post,
        'user': user,
        'title': 'Pioneer Partner - Edit Post',
    }

    return render(request, 'posts/edit_post.html', context)


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, post_id=post_id)
    post.delete()
    messages.success(request, 'Your post has been removed.')

    return redirect('dashboard')