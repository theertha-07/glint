from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from stories.models import Story, StoryStream
from stories.forms import NewStoryForm

from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt

from app.models import Follow 
from django.views.decorators.http import require_http_methods


@login_required
def NewStory(request):
    user = request.user

    if request.method == "POST":
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('content')
            caption = form.cleaned_data.get('caption')

            story = Story.objects.create(user=user, content=file, caption=caption)

            own_stream, created = StoryStream.objects.get_or_create(user=user, following=user)
            own_stream.story.add(story)

            followers = Follow.objects.filter(following=user)
            for follower in followers:
                follower_stream, created = StoryStream.objects.get_or_create(
                    user=follower.follower, following=user
                )
                follower_stream.story.add(story)

            return redirect('index')
    else:
        form = NewStoryForm()

    return render(request, 'newstory.html', {'form': form})


def ShowMedia(request, stream_id):
	stories = StoryStream.objects.get(id=stream_id)
	media_st = stories.story.all().values()

	stories_list = list(media_st)

	return JsonResponse(stories_list, safe=False)

from django.views.decorators.http import require_http_methods

@require_http_methods(["POST", "DELETE"])
@login_required
def delete_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    if story.user == request.user:
        story.delete()
        return JsonResponse({'success': True, 'message': 'Story deleted successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'You can only delete your own stories.'})




