from django.contrib import admin
from app.models import Post, Tag, Follow, Stream

# Register your models here.



admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
