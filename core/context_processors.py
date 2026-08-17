# core/context_processors.py
from .models import PdfCv

def ultimo_cv(request):
    # Retorna un diccionario con la variable que estará accesible en cualquier HTML
    return {
        'cv_actual': PdfCv.objects.first()
    }