from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

admin.site.register(User, UserAdmin) #так же надо переопределить параметр AUTH_USER_MODEL в setings