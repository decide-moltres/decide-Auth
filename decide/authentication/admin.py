from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    fields = ['related_political_party', 'birthdate ','sex  ','related_user  ']

admin.site.register(UserProfile, UserProfileAdmin)
# Register your models here.
