from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader

from app.models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.models import User
from app.forms import NewPostform
from authy.models import Profile

from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from django.db.models import Q  

from django.utils.timezone import now
from datetime import timedelta
from stories.models import StoryStream, Story
from django.db.models import Prefetch
# from django.utils.text import slugify

@login_required
def index(request):
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    
    profile = Profile.objects.get(user=user)

    # Posts from followed users via Stream
    stream_posts = Stream.objects.filter(user=user)
    followed_post_ids = [post.post_id for post in stream_posts]

    # Include user's own posts explicitly
    own_posts = Post.objects.filter(user=user).values_list('id', flat=True)
    
    # Merge and remove duplicates
    all_post_ids = list(set(followed_post_ids) | set(own_posts))

    # Final post list for feed
    post_items = Post.objects.filter(id__in=all_post_ids).order_by('-posted')

    # Optionally delete expired stories
    expiration_time = now() - timedelta(hours=24)
    Story.objects.filter(posted__lt=expiration_time).delete()

    active_stories = Story.objects.filter(posted__gte=expiration_time)

    story_streams = StoryStream.objects.filter(user=user).prefetch_related(
      Prefetch('story', queryset=active_stories),
          'following__profile'
       )

    filtered_streams = []
    my_stream = None
    

    for stream in story_streams:
      active_stories = stream.story.filter(posted__gte=expiration_time)
      if active_stories.exists():
        stream.story.set(active_stories)
        if stream.following == user:
           my_stream = stream
        else:
            filtered_streams.append(stream)

# Always show current user's story first
    if my_stream:
      filtered_streams.insert(0, my_stream)

    story_streams = filtered_streams

    user_story_stream = my_stream

    liked_users_data = {}
    for post in post_items:

        post.liked = Likes.objects.filter(user=request.user, post=post).exists()
        post.favourited = profile.favourite.filter(id=post.id).exists()
        post.liked_users = Likes.objects.filter(post=post).select_related('user__profile')[:3]
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        'story_streams': story_streams,
        'liked_users_data':liked_users_data,
        
        'user_story_stream': user_story_stream,
        # 'users_paginator': users_paginator,
    }
    return render(request, 'index.html', context)



@login_required
def NewPost(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')

            tag_form = form.cleaned_data.get('tags') or "" 

            tag_list = [tag.strip() for tag in tag_form.split(',') if tag.strip()]

            

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)

            p = Post.objects.create(picture=picture, caption=caption, user=user)
            if tags_obj: 
                p.tags.set(tags_obj)
            
            return redirect('profile', request.user.username)
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)


@login_required
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

   

    post.liked = Likes.objects.filter(user=user, post=post).exists()

    profile = Profile.objects.get(user=user)
    
    post.favourited = profile.favourite.filter(id=post.id).exists()


    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()


    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'liked': post.liked,
        
        
        
    }
    return render(request, 'postdetail.html', context)


@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    template = loader.get_template('tag.html')
    
    context = {
        'posts': posts,
        'tag': tag

    }

    return HttpResponse(template.render(context, request))


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


@login_required
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    
    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))
         



