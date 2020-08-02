from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Attendence

@admin.register(Attendence)
class AttendenceAdmin(ImportExportModelAdmin):
    pass