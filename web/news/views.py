from django.shortcuts import render

# Create your views here.
from django_tables2 import SingleTableView
from .models import News, NewsCategory
import django_tables2 as tables
from django.template import loader
from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404

class NewsTable(tables.Table):
    date = tables.DateTimeColumn(verbose_name='時間', attrs={"th": {"class": "contentNews bar3"}})
    title = tables.Column(verbose_name='標題', attrs={"th": {"class": "contentNews bar2"}})
    message = tables.Column(verbose_name='訊息', )
    class Meta:
        model = News
        template_name = "django_tables2/bootstrap.html"
        fields = ("date", "title", "message")
        attrs = {
            'class': 'contentNews bar'
        }

class NewsListView(SingleTableView):
    model = News
    table_class = NewsTable
    template_name = 'news.html'

def get_news(request, encrypted_id=""):
    news_category_filter = request.GET.get('news_category')
    print(news_category_filter)
    news_category = NewsCategory.objects.all()
    if news_category_filter:
        selected_category = NewsCategory.objects.filter(name=news_category_filter).first()
        news = News.objects \
                    .filter(category=selected_category) \
                    .filter(date__lt=datetime.datetime.now()) \
                    .order_by('date').all()
    else:
        news_category_filter = 'all'
        news = News.objects.filter(
            date__lt=datetime.datetime.now()
        ).order_by('date').all()
    currentTime = datetime.datetime.now().time()
    
    template = loader.get_template('news.html')
    context = {
        'news_category_filter': news_category_filter,
        'news_category': news_category,
        'news': news,
        'encrypted_id': encrypted_id,
        'now': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return HttpResponse(template.render(context, request))


def get_news_content(request, news_id):
    news = get_object_or_404(News, id=news_id)
    template = loader.get_template('news_content.html')
    context = {
        'news': news
    }
    return HttpResponse(template.render(context, request))