from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User
def home_page(request, encrypted_id=""):
    #you can check user here with request.user
    #example
    try:
        if encrypted_id:
            user = get_object_or_404(User, encrypted_id=encrypted_id)
            return render(request, 'player/home.html', {
                'encrypted_id': encrypted_id,
                'user': user
            })
        if request.user:
            if request.user.is_authenticated:
                if request.user.user_type == 'oc':
                    return redirect('/oc')
                elif request.user.user_type == 'admin':
                    return redirect('/oc')
            
        template = loader.get_template('error/error_message.html')
        context = {
            "message": "歡迎來到人生之旅，請使用手機掃描QR Code查看你的資料"
        }
        return HttpResponse(template.render(context, request))
    except:
        pass
    return render(request, 'login.html', {})


def handler404(request, exception):
    message = str(exception)  # Get the error message from the exception
    return render(request, 'error/404.html', {'error_message': message}, status=404)

# def handler500(request):
#     message = str(exception)  # Get the error message from the exception
#     return render(request, 'error/500.html', {'error_message': message}, status=500)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)