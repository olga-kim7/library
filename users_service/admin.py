from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users_service.models import User

admin.site.register(User, UserAdmin)