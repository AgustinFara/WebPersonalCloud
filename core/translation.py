from modeltranslation.translator import TranslationOptions, register

from .models import PdfCv


@register(PdfCv)
class ProyectTranslationOptions(TranslationOptions):
    fields = ['archivo_pdf']