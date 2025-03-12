from django.urls import path
from userauths import views


urlpatterns = [
    # Profile Section
    path('profile/edit', views.EditProfile, name="editprofile"),
]