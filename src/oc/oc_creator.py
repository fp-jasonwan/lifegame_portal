from account.models import User
for user in User.objects.all():
    if user.user_type == 'oc':
        user.set_password("Lionsoc2122")
        user.save()