from django.contrib import admin
from .models import News, NewsCategory
# Register your models here.

admin.site.register(News)
# admin.site.register(NewsCategory)

class NewsInline(admin.TabularInline):
    model = News

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsInline]

admin.site.register(NewsCategory, NewsAdmin)