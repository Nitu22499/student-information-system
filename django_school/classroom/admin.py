from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import User,Student,Teacher,Subject

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Subject)
# admin.site.register(User)