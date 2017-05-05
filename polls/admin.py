# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import file_record

class FilesAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'owner', 'date']


# Register your models here.
admin.site.register(file_record, FilesAdmin)
