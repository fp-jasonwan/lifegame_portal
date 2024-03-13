from django.contrib import admin
from .models import News, NewsCategory
# Register your models here.

admin.site.register(News)
# admin.site.register(NewsCategory)

class NewsInline(admin.TabularInline):
    model = News
    list_display = ('id', 'name',)

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsInline]
    list_display = ('id', 'title', 'category')

admin.site.register(NewsCategory, NewsAdmin)