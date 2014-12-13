from django.contrib import admin
from datagetter.models import PostingImages, Postings


# Register your models here.
class PostingsAdmin(admin.ModelAdmin):

    list_display = ('id', 'link', 'title')


admin.site.register(Postings, PostingsAdmin)
admin.site.register(PostingImages)