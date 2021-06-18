from django.contrib import admin
from .models import Image, Contribute, Sponsor, New

# Register your models here.
class AdminImages(admin.ModelAdmin):
    list_display = ("id", "name", "upload_in")
    list_display_links = ("id", "name", "upload_in")
    search_fields = ("id", "name", "upload_in", "image")
    list_per_page = 20


class AdminNews(admin.ModelAdmin):
    list_display = ("id", "title", "poster", "abstract", "posted_in")
    list_display_links = ("id", "title", "poster", "abstract", "posted_in")
    search_fields = ("id", "title", "poster", "abstract", "posted_in", "content")
    list_per_page = 20


admin.site.register(Image, AdminImages)
admin.site.register(Contribute)
admin.site.register(Sponsor)
admin.site.register(New, AdminNews)
