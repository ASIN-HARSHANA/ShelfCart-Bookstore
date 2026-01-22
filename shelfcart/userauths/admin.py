from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ContactUs,Profile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['email', 'username','is_staff', 'is_active']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject'] 

#class ProfileAdmin(admin.ModelAdmin):
#    list_display = ['user','full_name', 'bio', 'phone'] 


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile)

