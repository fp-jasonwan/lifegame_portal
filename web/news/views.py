from django.shortcuts import render

# Create your views here.
from django_tables2 import SingleTableView
from .models import News, NewsCategory
import django_tables2 as tables
from django.template import loader
from django.http import HttpResponse
import datetime
class NewsTable(tables.Table):
    time = tables.DateTimeColumn(verbose_name='時間', attrs={"th": {"class": "contentNews bar3"}})
    title = tables.Column(verbose_name='標題', attrs={"th": {"class": "contentNews bar2"}})
    message = tables.Column(verbose_name='訊息', )
    class Meta:
        model = News
        template_name = "django_tables2/bootstrap.html"
        fields = ("time", "title", "message")
        attrs = {
            'class': 'contentNews bar'
        }

class NewsListView(SingleTableView):
    model = News
    table_class = NewsTable
    template_name = 'news.html'

def get_news(request, encrypted_id=""):
    currentTime = datetime.datetime.now().time()
    news = News.objects.filter().order_by('time').all()
    template = loader.get_template('news.html')
    context = {
        'news': news,
        'encrypted_id': encrypted_id,
    }
    return HttpResponse(template.render(context, request))