from django.contrib import admin
from .models        import Project, Course
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

admin.site.register(Project)

class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Course)