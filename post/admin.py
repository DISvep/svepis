from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from .models import Post, Announcement


class PostAdmin(admin.ModelAdmin):
    list_filter = ['user', 'date']
    list_display = ['user', 'date']
    search_fields = ['user__username', 'date']
    
    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Announcement)
