from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FacebookMember

admin.site.register(FacebookMember, UserAdmin)
