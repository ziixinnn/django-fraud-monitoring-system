from django.contrib import admin
from .models import Staff

class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'role', 'created_at', 'updated_at')

admin.site.register(Staff, StaffAdmin)