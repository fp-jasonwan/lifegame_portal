from django.shortcuts import render
from django.template import RequestContext


def handler404(request, exception, template_name='error/404.html'):
    # response = render_to_response('404.html', {},
    #                               context_instance=RequestContext(request))
    # response.status_code = 404
    print('404')
    return render(request, template_name)


def handler500(request, exception, template_name='error/500.html'):
    print('500')
    return render(request, template_name)