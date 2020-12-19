from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
# Create your views here.

def oc_portal(request):
    if request.user.user_type == 'student':
        return redirect('/404')
    return render(request, 'oc/oc_portal.html')

def search_profile(request):
    # profile = get_object_or_404(Student, user=request.user)
    template = loader.get_template('oc/search_profile.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
    # return HttpResponse("You're voting on question %s." % question_id)