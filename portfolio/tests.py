from datetime import date

from django.test import TestCase

from .models import Course, Project


class ProjectModelTest(TestCase):
    def setUp(self):
        # Creamos un proyecto de prueba
        self.project = Project.objects.create(
            title="Proyecto Test",
            description="Descripción de prueba",
            date=date(2023, 5, 25)
        )

    def test_project_creation(self):
        """Verifica que el modelo se cree con los datos correctos"""
        self.assertEqual(self.project.title, "Proyecto Test")
        self.assertEqual(str(self.project), "Proyecto Test")

    def test_project_ordering(self):
        """Verifica que el orden sea por fecha descendente"""
        Project.objects.create(title="Proyecto Antiguo",
                               description="...", date=date(2020, 1, 1))
        projects = Project.objects.all()
        # El proyecto más reciente (2023) debería estar en la posición 0
        self.assertEqual(projects[0].title, "Proyecto Test")


class CourseModelTest(TestCase):
    def setUp(self):
        # Creamos dos cursos para probar el ordenamiento
        self.course1 = Course.objects.create(
            title="Curso 1",
            description="Desc 1",
            date=date(2021, 1, 1)
        )
        self.course2 = Course.objects.create(
            title="Curso 2",
            description="Desc 2",
            date=date(2022, 1, 1)
        )

    def test_course_creation(self):
        self.assertEqual(str(self.course1), "Curso 1")

    def test_course_ordering(self):
        """Verifica que el curso más nuevo (2022) aparezca primero"""
        courses = Course.objects.all()
        self.assertEqual(courses[0].title, "Curso 2")
        self.assertEqual(courses[1].title, "Curso 1")

    def test_pdf_field_is_optional(self):
        """Verifica que el campo del PDF pueda estar vacío (blank/null)"""
        course = Course.objects.create(
            title="Curso sin PDF",
            description="...",
            date=date(2023, 1, 1)
        )
        self.assertIsNone(course.archivo_pdf.name)
