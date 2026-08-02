import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from .models import Work


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class WorkModelTests(TestCase):
    def test_date_started_english(self):
        settings.LANGUAGE_CODE = 'en-US'
        test_date = datetime.datetime(2010, 1, 3)
        work_english = Work(datestart=test_date,
                            title='test_en', company='django')
        self.assertEqual(work_english.date_started(), 'January 2010')

    def test_date_started_german(self):
        settings.LANGUAGE_CODE = 'de-DE'
        test_date = datetime.datetime(1987, 12, 7)
        work_german = Work(datestart=test_date,
                           title='test_de', company='django')
        self.assertEqual(work_german.date_started(), 'Dezember 1987')

    def test_date_started_italian(self):
        settings.LANGUAGE_CODE = 'it-IT'
        test_date = datetime.datetime(1950, 10, 11)
        work_italian = Work(datestart=test_date,
                            title='test_it', company='django')
        self.assertEqual(work_italian.date_started(), 'Ottobre 1950')

    def test_date_finished_french(self):
        settings.LANGUAGE_CODE = 'fr-FR'
        test_date = datetime.datetime(2018, 2, 9)
        work_french = Work(datefinish=test_date,
                           title='test_fr', company='django')
        self.assertEqual(work_french.date_finished(), 'Février 2018')

    def test_date_finished_portuguese(self):
        settings.LANGUAGE_CODE = 'pt-BR'
        test_date = datetime.datetime(1987, 11, 25)
        work_portuguese = Work(datefinish=test_date,
                               title='test_br', company='django')
        self.assertEqual(work_portuguese.date_finished(), 'Novembro 1987')

    def test_date_finished_greek(self):
        settings.LANGUAGE_CODE = 'el-EL'
        test_date = datetime.datetime(1920, 4, 15)
        work_greek = Work(datefinish=test_date,
                          title='test_el', company='django')
        self.assertEqual(work_greek.date_finished(), 'Απριλίου 1920')

    def test_dates_time_worked(self):
        test_date_st = datetime.datetime(1920, 4, 15)
        test_date_fi = datetime.datetime(1940, 6, 15)
        work_diff = Work(datestart=test_date_st,
                         datefinish=test_date_fi, title='test_diff')
        self.assertEqual(work_diff.time_worked(), '20 años y 2 meses')

    def test_dates_time_worked_less_than_month(self):
        test_date_st = datetime.datetime(1990, 4, 15)
        test_date_fi = datetime.datetime(1990, 5, 10)
        work_diff = Work(datestart=test_date_st,
                         datefinish=test_date_fi, title='test_diff')
        self.assertEqual(work_diff.time_worked(), 'Menos de un mes')

    def test_dates_time_worked_one_month(self):
        test_date_st = datetime.datetime(1989, 12, 15)
        test_date_fi = datetime.datetime(1990, 1, 14)
        work_diff = Work(datestart=test_date_st,
                         datefinish=test_date_fi, title='test_diff')
        self.assertEqual(work_diff.time_worked(), '1 mes')

    def test_dates_time_worked_less_than_month_exact(self):
        test_date_st = datetime.datetime(1989, 12, 15)
        test_date_fi = datetime.datetime(1990, 1, 13)
        work_diff = Work(datestart=test_date_st,
                         datefinish=test_date_fi, title='test_diff')
        self.assertEqual(work_diff.time_worked(), 'Menos de un mes')

    def test_dates_time_worked_year_and_month(self):
        test_date_st = datetime.datetime(1980, 5, 1)
        test_date_fi = datetime.datetime(1981, 6, 1)
        work_diff = Work(datestart=test_date_st,
                         datefinish=test_date_fi, title='test_diff')
        self.assertEqual(work_diff.time_worked(), '1 año y 1 mes')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestEdadAbout(TestCase):

    def setUp(self):
        self.client = Client()
        translation.activate('es')
        self.url = reverse('cv:about')
        

    @patch('cv.views.timezone.localdate')
    def test_edad_calculada_correctamente_en_cumpleaños(self, mock_localdate):
        """Prueba que si hoy es el cumpleaños de 2024, la edad sea exactamente 40"""
        # Le decimos a localdate() que devuelva DIRECTAMENTE el objeto fecha
        mock_localdate.return_value = datetime.date(2024, 3, 4)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['edad'], 40)

    @patch('cv.views.timezone.localdate')
    def test_edad_un_dia_antes_del_cumpleaños(self, mock_localdate):
        """Prueba que si hoy es un día antes de tu cumple en 2024, todavía devuelva 39"""
        # Le decimos a localdate() que devuelva DIRECTAMENTE el objeto fecha
        mock_localdate.return_value = datetime.date(2024, 3, 3)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['edad'], 39)

    def tearDown(self):
        translation.deactivate() # Buena práctica: desactivar al terminar el test


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestExpAbout(TestCase):

    def setUp(self):
        self.client = Client()
        translation.activate('es')
        self.url = reverse('cv:about')

    def test_experiencia_mainframe_redondea_hacia_arriba_con_10_meses(self):
        """Prueba que Julio 2006 a Mayo 2026 (19 años, 10 meses) devuelva 20 años"""
        # Creamos un trabajo de prueba en la BD temporal que contenga la palabra "Mainframe"
        Work.objects.create(
            title="Puesto Test 1",
            company="Empresa Test",
            description="Desarrollador en entorno Mainframe",
            datestart=datetime.date(2006, 7, 1),
            datefinish=datetime.date(2026, 5, 1),
            image="test.png"
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Verificamos que tu regla de los 9 meses haya sumado el año entero (19 + 1 = 20)
        self.assertEqual(response.context['exp_mainframe'], 20)

    def test_experiencia_mainframe_no_redondea_con_menos_de_9_meses(self):
        """Prueba que Julio 2006 a Marzo 2026 (19 años, 8 meses) devuelva 19 años"""
        # Limpiamos por las dudas trabajos anteriores en este test
        Work.objects.all().delete()

        # Creamos un período que da justo 19 años y 8 meses (no llega a tu regla de 9)
        Work.objects.create(
            title="Puesto Test 2",
            company="Empresa Test",
            description="Analista Mainframe Senior",
            datestart=datetime.date(2006, 7, 1),
            datefinish=datetime.date(2026, 3, 1),
            image="test.png"
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # Como son 8 meses restantes, tiene que quedarse en los 19 años base
        self.assertEqual(response.context['exp_mainframe'], 19)

    def tearDown(self):
        translation.deactivate() # Buena práctica: desactivar al terminar el test
