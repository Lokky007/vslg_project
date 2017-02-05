from django.contrib import admin
from main.models import file_record

class FilesAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['file_name']}),
                 ('Date Information', {'fields': ['date'],
                 'classes': ['collapse']}),
                 ]

class MyAdminSite(admin.ModelAdmin):
    site_header = 'Monty Python administration'

# Register your models here.
admin.site.register(file_record, FilesAdmin);
