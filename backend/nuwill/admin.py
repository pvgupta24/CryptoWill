from django.contrib import admin

from .models import UserNextKin, UserSecret

admin.site.register(UserSecret)
admin.site.register(UserNextKin)
