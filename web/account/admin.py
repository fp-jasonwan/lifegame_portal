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

class UserInline(admin.StackedInline):
    model = User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_per_page = 10
    list_display = ('id', 'username', 'last_name','first_name', 'school', 'instructor_group')
    search_fields = ('username','first_name', 'last_name', 'school')
    ordering = ('id',)
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_type', 'encrypted_id', 'instructor_group')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'nick_name', 'email', 'mobile', 'school', 'school_code',)}), 
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
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

@admin.register(InstructorGroup)
class InstructorGroupAdmin(admin.ModelAdmin):
    pass
    # inlines = [UserInline]