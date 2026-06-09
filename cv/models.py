from django.db import models
from babel import Locale
from django.conf import settings
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre de categoría")
    order = models.IntegerField(default=0, verbose_name="Orden de visualización")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Cronomarcador de creación")
    updated = models.DateTimeField(auto_now =True, verbose_name = "Cronomarcador de modificación")

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['order'] # Esto permite que siempre se listen ordenadas

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoría", related_name="technologies", null=True, blank=True)    
    order = models.IntegerField(default=0, verbose_name="Orden de visualización")
    icon_svg = models.TextField(help_text="Pega aquí el código SVG")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Cronomarcador de creación")
    updated = models.DateTimeField(auto_now =True, verbose_name = "Cronomarcador de modificación")

    class Meta:
        verbose_name = 'Tecnología'
        verbose_name_plural = 'Tecnologías'
        ordering = ['order']



    def __str__(self):
        return self.name


# Create your models here.
class Work(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Título")
    company = models.CharField(max_length=200, verbose_name = "Empresa")
    description = models.TextField(verbose_name = "Descripción")
    image = models.ImageField(verbose_name = "Imagen", upload_to = "work")
    datestart = models.DateField(verbose_name = "Fecha de comienzo")
    datefinish = models.DateField(verbose_name = "Fecha de finalización", null=True, blank=True)
    is_current = models.BooleanField(default=False, verbose_name="¿Es mi trabajo actual?")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Cronomarcador de creación")
    updated = models.DateTimeField(auto_now =True, verbose_name = "Cronomarcador de modificación")

    class Meta:
        verbose_name = 'Trabajo'
        verbose_name_plural = 'Trabajos'
        ordering = ['-datestart']
#        ordering = ['-datefinish'] Lo cambio a datestart porque permito nulls por nuevo campo is_current

    def clean(self):
            # Si NO es el trabajo actual, datefinish es obligatorio
            if not self.is_current and self.datefinish is None:
                raise ValidationError({
                    'datefinish': "Debes ingresar una fecha de finalización si este no es tu trabajo actual."
                })
            
            # Opcional: Si ES el trabajo actual, asegúrate de que datefinish sea None (limpieza)
            if self.is_current:
                self.datefinish = None


    def __str__(self):
        return ( self.title + ' en ' + self.company )

    def date_started(self):
            locale = Locale(settings.LANGUAGE_CODE[:2])
            month = self.datestart.strftime("%m")
            month_localized = locale.months['format']['wide'][int(month)]
            return (str(month_localized.title()) + " " + self.datestart.strftime("%Y"))

    def date_finished(self):
            locale = Locale(settings.LANGUAGE_CODE[:2])
            month = self.datefinish.strftime("%m")
            month_localized = locale.months['format']['wide'][int(month)]
            return (str(month_localized.title()) + " " + self.datefinish.strftime("%Y"))

    def time_worked(self):
        months = ( self.datefinish.year - self.datestart.year) * 12 + self.datefinish.month - self.datestart.month
        years = months // 12
        months = months - ( years * 12 )

        if years > 1:
            year_name = ' años'
        else:
            year_name = ' año'

        if months > 1:
            month_name = ' meses'
        else:
            month_name = ' mes'

        if years == 0:
            if months == 1:
                days_diff =  self.datefinish - self.datestart
                if days_diff.days < 30:
                    return('Menos de un mes')
                else:
                    return(str(months) + month_name)
            else:
                return(str(months) + month_name)
        else:
            if months == 0:
                return(str(years) + year_name)
            else:
                return(str(years) + year_name + ' y ' + str(months) + month_name)

class Client(models.Model):
    client = models.ForeignKey(Work, on_delete=models.CASCADE, verbose_name = "Empresa Cliente")
    company = models.CharField(blank=True, null=True, max_length=200, verbose_name = "Empresa Cliente")
    image = models.ImageField(blank=True, null=True, verbose_name = "Imagen Cliente", upload_to = "work")
    description = models.TextField(blank=True, null=True,verbose_name = "Descripción")
    datestart = models.DateField(verbose_name = "Fecha de comienzo")
    datefinish = models.DateField(verbose_name = "Fecha de finalización")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Cronomarcador de creación")
    updated = models.DateTimeField(auto_now =True, verbose_name = "Cronomarcador de modificación")

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-datefinish']

    def __str__(self):
        return f"{self.company} cliente de {self.client.company}"

    def date_started(self):
            locale = Locale(settings.LANGUAGE_CODE[:2])
            month = self.datestart.strftime("%m")
            month_localized = locale.months['format']['wide'][int(month)]
            return (str(month_localized.title()) + " " + self.datestart.strftime("%Y"))

    def date_finished(self):
            locale = Locale(settings.LANGUAGE_CODE[:2])
            month = self.datefinish.strftime("%m")
            month_localized = locale.months['format']['wide'][int(month)]
            return (str(month_localized.title()) + " " + self.datefinish.strftime("%Y"))

    def time_worked(self):
        months = ( self.datefinish.year - self.datestart.year) * 12 + self.datefinish.month - self.datestart.month
        years = months // 12
        months = months - ( years * 12 )

        if years > 1:
            year_name = ' años'
        else:
            year_name = ' año'

        if months > 1:
            month_name = ' meses'
        else:
            month_name = ' mes'

        if years == 0:
            if months == 1:
                days_diff =  self.datefinish - self.datestart
                if days_diff.days < 30:
                    return('Menos de un mes')
                else:
                    return(str(months) + month_name)
            else:
                return(str(months) + month_name)
        else:
            if months == 0:
                return(str(years) + year_name)
            else:
                return(str(years) + year_name + ' y ' + str(months) + month_name)
