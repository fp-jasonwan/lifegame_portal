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
from news.views import NewsListView
from account.views import home_page

urlpatterns = [
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', home_page, name='home'),
    path('oc_portal/', include('oc.urls')),
    path('test', TemplateView.as_view(template_name='test.html'), name='test'),
    path('admin/', admin.site.urls),
    path('accounts/', include('account.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('player.urls')),
    path('news/', NewsListView.as_view()),
    path('404', TemplateView.as_view(template_name='error/404.html'), name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)