from django.shortcuts import render, redirect

def home_page(request, user_id=""):
    #you can check user here with request.user
    #example
    try:
        if request.user.is_authenticated and request.user.is_active:

            # if request.user.user_type == 'student':
            #     return render(request, 'player/home.html', {})
            if request.user.user_type == 'oc':
                return render(request, 'oc/home.html', {})
            elif request.user.user_type == 'admin':
                return render(request, 'oc/home.html', {})
            elif request.user.user_type == 'instructor':
                return render(request, 'oc/home.html', {})
        return render(request, 'player/home.html', {
                'user_id': user_id
        })
    except:
        pass
    return render(request, 'login.html', {})
