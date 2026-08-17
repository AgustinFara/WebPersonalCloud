from django.contrib import admin

from .models import PdfCv


class PdfCvAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")


admin.site.register(PdfCv)