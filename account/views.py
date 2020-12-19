from django.shortcuts import render, redirect

def home_page(request):
    #you can check user here with request.user
    #example
    if request.user.user_type == 'student':
        return render(request, 'player/home.html', {})
    elif request.user.user_type == 'oc':
        return render(request, 'oc/home.html', {})
    return render(request, 'home.html', {})
