from django.shortcuts import render

# Create your views here.
from django_tables2 import SingleTableView
from .models import News
import django_tables2 as tables

class NewsTable(tables.Table):
    class Meta:
        model = News
        template_name = "django_tables2/bootstrap.html"
        fields = ("message", )

class NewsListView(SingleTableView):
    model = News
    table_class = NewsTable
    template_name = 'news.html'
