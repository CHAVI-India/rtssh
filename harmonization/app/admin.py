
from django.contrib import admin
from .models import LabelMapping
from .models import UploadedFile, ProcessedFile, TG263Data

# Register your models here.
@admin.register(LabelMapping)
class LabelMappingAdmin(admin.ModelAdmin):
    list_display = ('original_label', 'TG263_label',)

# admin.py
@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('file',)

@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = ('file',)


@admin.register(TG263Data)
class LabelMappingAdmin(admin.ModelAdmin):
    list_display = ('Anatomic_Group', 'TG263_Primary_Name', 'Description',)



admin.sites.AdminSite.site_header = 'CLI Administration'
