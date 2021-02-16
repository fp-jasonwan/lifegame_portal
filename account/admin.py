from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('icon',)

    def is_complete(self, obj):
        # Example here, you can use any expression.
        return SomeOtherClass.objects.get(my_field=obj).is_complete()

    # Not required, but this gives you a nice boolean field:
    is_complete.boolean = True

# admin.site.register(User, UserAdmin)
admin.site.register(User, CustomUserAdmin)