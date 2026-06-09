from django.contrib import admin
from .models         import Work
from .models         import Client
from .models         import Technology
from .models         import Category
from django.core.exceptions import ValidationError

# Register your models here.

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")  
    list_display = ('title', 'company', 'is_current', 'datefinish')
    list_editable = ('is_current',) # Para marcarlo rápido desde la lista

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

@admin.register(Category)
class CatAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
    list_display = ('name', 'order')
    list_editable = ('order',) # Para marcarlo rápido desde la lista

@admin.register(Technology)
class TechAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated",)
    list_display = ('name', 'category', 'order')
    list_editable = ('category', 'order',) # Para marcarlo rápido desde la lista
