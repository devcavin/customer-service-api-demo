from django.contrib import admin

# Register your models here.

from c_service.models import Notes

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "updated_at")