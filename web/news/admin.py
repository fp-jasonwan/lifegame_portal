from django.contrib import admin
from .models import News, NewsCategory
# Register your models here.

# class NewsCategoryInline(admin.TabularInline):
    # model = NewsCategory

class NewsAdmin(admin.ModelAdmin):
    # inlines = [NewsCategoryInline]
    list_display = ('id', 'title', 'category',)


admin.site.register(News, NewsAdmin)
# admin.site.register(NewsCategory)

class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

admin.site.register(NewsCategory, NewsCategoryAdmin)