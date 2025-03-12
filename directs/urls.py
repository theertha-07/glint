from django.urls import path
from directs import views

urlpatterns = [
    path('inbox/', views.inbox, name="message"),
    path('directs/<username>', views.Directs, name="directs"),
    # path('send/', views.SendMessage, name="send-message"),
    path('send/', views.SendDirect, name="send-directs"),
    # path('new/', views.UserSearch, name="user-search"),
    path('search/', views.UserSearch, name="search-users"),
    path('new/<username>', views.NewConversation, name="conversation"),

]