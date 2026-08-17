from django.db import models


class PdfCv(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    archivo_pdf = models.FileField(
        blank=True, null=True, verbose_name="Certificado PDF", upload_to='core/pdf_cv/')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Cronomarcador de creación")
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Cronomarcador de modificación")

    class Meta:
        verbose_name = 'PDF CV'
        verbose_name_plural = 'PDF CVs'

    def __str__(self):
        return self.title
