"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from news.views import NewsListView, get_news
from account.views import home_page
from booth.views import BoothsListView, get_booths_map, redirect_zoom
from oc.views import get_contact
from player.views import get_rich_list, get_score_list
handler404 = 'main.views.handler404'
handler403 = 'main.views.handler403'

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', home_page, name='home'),
    path('oc/', include('oc.urls')),
    path('test', TemplateView.as_view(template_name='test.html'), name='test'),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('player/<str:encrypted_id>/', include('player.urls')),
    path('news/', get_news),
    path('booths/', get_booths_map),
    path('booths/<str:booth_id>', redirect_zoom),
    path('contact/', get_contact, name='contact'),
    path('rich_list/', get_rich_list),
    path('score_list/', get_score_list),
    path('map/', TemplateView.as_view(template_name='map.html'), name='map'),
    path('rules/', TemplateView.as_view(template_name='rules.html'), name='rules'),
    path('404', TemplateView.as_view(template_name='error/404.html'), name='404'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)