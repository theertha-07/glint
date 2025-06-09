from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from directs.models import Message
from authy.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from django.utils.timezone import now
from datetime import timedelta

def format_message_date(dt):
    diff = now() - dt
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return dt.strftime("%d %b, %Y")  

@login_required
def inbox(request):
    user = request.user

    messages = Message.get_messages(user=request.user)


    if not messages:  
        messages = []

    active_direct = None
    directs = None
    profile = get_object_or_404(Profile, user=user)

    if messages:
        first_message = messages[0]
        message = messages[0]
        active_direct = message['user'].username
        directs = Message.objects.filter(user=request.user, recipient=message['user']) 
        directs.update(is_read=True)  
        for direct in directs:
           direct.display_date = format_message_date(direct.date)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
    }
    
    return render(request, 'directs/direct.html', context)

@login_required
def Directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)

    active_direct = username
    
    directs = Message.objects.filter(user=user, recipient__username=username)  
    directs.update(is_read=True) 

    for direct in directs:
        direct.display_date = format_message_date(direct.date)

 
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }
    
    return render(request, 'directs/direct.html', context)

    
def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))
    
        
        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            }

    return render(request, 'directs/search.html', context)

def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('search-users')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('message')

@login_required
def SendDirect(request):
    if request.method == "POST":
        from_user = request.user
        to_user_username = request.POST.get('to_user')
        body = request.POST.get('body', '').strip()  

        if not body:

            return redirect('message') 

        try:
            to_user = User.objects.get(username=to_user_username)
        except User.DoesNotExist:
            return HttpResponseBadRequest("Recipient does not exist.")

        Message.send_message(from_user, to_user, body)
        return redirect('message')

def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}






