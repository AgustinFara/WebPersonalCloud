from modeltranslation.translator import TranslationOptions, register

from .models import Category, Work, Client


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']

@register(Work)
class WorkTranslationOptions(TranslationOptions):
    fields = ['title', 'description']

@register(Client)
class ClientTranslationOptions(TranslationOptions):
    fields = ['description']