from django.contrib import admin
from .models import News, NewsCategory
# Register your models here.

class NewsInline(admin.TabularInline):
    model = News

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsInline]
    list_display = ('id', 'title', 'category')


admin.site.register(News, NewsAdmin)
# admin.site.register(NewsCategory)

class NewsCategoryInline(admin.TabularInline):
    model = NewsCategory

class NewsCategoryAdmin(admin.ModelAdmin):
    inlines = [NewsCategoryInline]
    list_display = ('id', 'name')

admin.site.register(NewsCategory, NewsCategoryAdmin)