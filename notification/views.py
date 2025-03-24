import importlib
from django.shortcuts import render, redirect
from notification.models import Notification

#new change!!!!
from django.template import loader
from django.http import HttpResponse


def ShowNotification(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    # #new change!!!
    # Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    
    # template = loader.get_template('notifications/notification.html')

    context = {
        'notifications': notifications,

    }
    return render(request, 'notifications/notification.html', context)

    # return HttpResponse(template.render(context, request))

def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notification')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}

# Create your views here.
