"""
URL configuration for glint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from userauths.models import Profile
from userauths.views import UserProfile, follow
# from directs.views import inbox, Directs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('userauths.urls')),
    path('post/', include('app.urls')),
    path('message/', include('directs.urls')),
   

    # Profile url section
    path('<username>/', UserProfile, name="profile"),
    path('<username>/saved/', UserProfile, name="profilefavourite"),
    path('<username>/follow/<option>/', follow, name="follow"),


]


# This is used for
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
