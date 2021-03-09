from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse

def handler404(request, exception, template_name='error/404.html'):
    print('404')
    return render(request, template_name)


def handler500(request, exception, template_name='error/500.html'):
    print('500')
    return render(request, template_name)
