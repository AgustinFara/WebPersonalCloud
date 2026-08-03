from modeltranslation.translator import TranslationOptions, register

from .models import Project, Course


@register(Project)
class ProyectTranslationOptions(TranslationOptions):
    fields = ['title','description']

@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ['title','description']