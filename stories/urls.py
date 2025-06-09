from django.urls import path
from stories.views import NewStory, ShowMedia, delete_story

urlpatterns = [
	path('newstory/', NewStory, name='newstory'),
	path('showmedia/<stream_id>', ShowMedia, name='showmedia'),
    path('delete_story/<int:story_id>/', delete_story, name='delete_story'),
   
]