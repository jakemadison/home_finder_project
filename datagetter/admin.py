from django.contrib import admin
from datagetter.models import PostingImages, Postings, PostingRating


# Register your models here.
class PostingsAdmin(admin.ModelAdmin):

    list_display = ('id', 'link', 'title')


class PostingRatingAdmin(admin.ModelAdmin):

    list_display = ('posting', 'positive_rating')


admin.site.register(Postings, PostingsAdmin)
admin.site.register(PostingImages)
admin.site.register(PostingRating, PostingRatingAdmin)