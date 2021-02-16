from django.shortcuts import render

# Create your views here.
from django_tables2 import SingleTableView
from .models import News
import django_tables2 as tables

class NewsTable(tables.Table):
    time = tables.Column(verbose_name='時間')
    title = tables.Column(verbose_name='標題')
    message = tables.Column(verbose_name='訊息')
    class Meta:
        model = News
        template_name = "django_tables2/bootstrap.html"
        fields = ("time", "title", "message")
        attrs = {
            'class': 'table table-bordered dataTable'
        }

class NewsListView(SingleTableView):
    model = News
    table_class = NewsTable
    template_name = 'news.html'
