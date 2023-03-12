from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, InstructorGroup
from player.models import Player
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     list_display = UserAdmin.list_display + ('icon',)


# # admin.site.register(User, UserAdmin)
# admin.site.register(User, CustomUserAdmin)
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class PlayerInline(admin.StackedInline):
    model = Player

class MyUserAdmin(UserAdmin):
    list_per_page = 10
    list_display = ('id', 'school',)
    search_fields = ('id','first_name', 'last_name', 'school')
    ordering = ('id',)
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type', 'encrypted_id')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'nick_name', 'email', 'mobile')}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 
        # 'groups', 'user_permissions'
        )}), 
        ('Important dates', {'fields': ('last_login', 'date_joined', )}),
    )
    # inlines = [
    #     PlayerInline,
    # ]
    # fieldsets =  (
    #     (None, {
    #         'fields': ('user_type', 'nick_name', 'icon',),
    #         'personal': ()
    #     }),
    # )

admin.site.register(User, MyUserAdmin)
admin.site.register(InstructorGroup)