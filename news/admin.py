from django.contrib import admin

from .models import News, Tag

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    model = News
    

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = News