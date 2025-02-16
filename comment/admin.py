from django.contrib import admin
from .models import PostComment, VideoComment


# Register your models here.
admin.site.register(PostComment)
admin.site.register(VideoComment)
