from django.contrib import admin
from .models import GeneratedImage

@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ("user", "prompt", "image_url", "created_at")
    search_fields = ("prompt", "user__username")
