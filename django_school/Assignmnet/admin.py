from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Student,Teacher

from Assignmnet.models import Assignment
# Register your models here.
admin.site.register(Assignment)