import importlib
from django.shortcuts import render, redirect
from notification.models import Notification

from django.template import loader
from django.http import HttpResponse

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


def ShowNotification(request):
    user = request.user
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    notifications = Notification.objects.filter(user=user).order_by('-date')
    
    template = loader.get_template('notifications/notification.html')

    context = {
        'notifications': notifications,

    }
    return HttpResponse(template.render(context, request))

@login_required
@require_POST
def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notification')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}



