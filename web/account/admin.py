from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     list_display = UserAdmin.list_display + ('icon',)


# # admin.site.register(User, UserAdmin)
# admin.site.register(User, CustomUserAdmin)
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'nick_name', 'email', 'mobile')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
        # 'groups', 'user_permissions'
        )}), 
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    # fieldsets =  (
    #     (None, {
    #         'fields': ('user_type', 'nick_name', 'icon',),
    #         'personal': ()
    #     }),
    # )

admin.site.register(User, MyUserAdmin)