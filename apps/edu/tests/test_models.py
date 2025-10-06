import datetime
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.edu.models import (
    Major,
    Field,
    Professor,
    Education,
    Publication,
    Course,
    University,
    UniversityImage,
    Position,
    DegreeChoices,
    Authorship,
    Teaching,
    UniversityCourse,
)


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.content = b"hello world!"
        cls.photo = SimpleUploadedFile("test.jpg", cls.content, "image/jpeg")
        cls.file = SimpleUploadedFile("file.txt", cls.content, "text/plain")

        cls.major = Major.objects.create(title="major", degree="BACHELOR")
        
        cls.field = Field.objects.create(title="field")
        cls.field.majors.add(cls.major)
        
        cls.professor = Professor.objects.create(
            first_name="professor",
            last_name="professor",
            email="test@email.com",
            phone="0",
            biography="test",
            photo=cls.photo,
        )
        cls.professor.fields.add(cls.field)
        
        cls.publication = Publication.objects.create(title="test", file=cls.file)
        # cls.publication.authors.add(cls.professor)
        Authorship.objects.create(professor=cls.professor, publication=cls.publication)

        cls.course = Course.objects.create(
            title="test",
            major=cls.major,
            period=20,
            price=2000,
            is_accessible=True,
        )
        # cls.course.professors.add(cls.professor)
        Teaching.objects.create(professor=cls.professor, course=cls.course)

        cls.university = University.objects.create(
            name="test",
            logo=cls.photo,
        )
        # cls.university.professors.add(cls.professor)
        # cls.university.courses.add(cls.course)
        UniversityCourse.objects.create(university=cls.university, course=cls.course)
        cls.university.majors.add(cls.major)

        cls.university_image = UniversityImage.objects.create(
            image=cls.photo, university=cls.university
        )

        cls.position = Position.objects.create(
            title="test",
            description="test here",
            university=cls.university,
            professor=cls.professor,
            major=cls.major,
            deadline=datetime.date.today(),
        )

        cls.professor.university = cls.university

        cls.education = Education.objects.create(
            professor=cls.professor,
            major=cls.major,
            university=cls.university,
            graduation_year=2000,
        )


    def test_major(self):
        major = self.major
        self.assertEqual(major.title, "major")
        self.assertEqual(major.degree, DegreeChoices.BACHELOR_CHOICE)

    def test_field(self):
        self.assertEqual(self.field.title, "field")
        self.assertEqual(len(self.field.majors.all()), 1)
        self.assertIn(self.major, self.field.majors.all())

    def test_professor(self):
        professor = self.professor
        self.assertEqual(professor.first_name, "professor")
        self.assertEqual(professor.last_name, "professor")
        self.assertEqual(professor.email, "test@email.com")
        self.assertEqual(professor.phone, "0")
        self.assertEqual(professor.biography, "test")
        professor.photo.open()
        self.assertEqual(professor.photo.read(), self.content)
        professor.photo.close()
        self.assertEqual(len(professor.fields.all()), 1)
        self.assertIn(self.field, professor.fields.all())
        self.assertEqual(professor.university, self.university)

    def test_publication(self):
        publication = self.publication
        self.assertEqual(publication.title, "test")
        publication.file.open()
        self.assertEqual(publication.file.read(), self.content)
        publication.file.close()
        self.assertEqual(len(publication.authors.all()), 1)
        self.assertIn(self.professor, publication.authors.all())

    def test_course(self):
        course = self.course
        self.assertEqual(course.title, "test")
        self.assertEqual(course.major, self.major)
        self.assertEqual(course.period, 20)
        self.assertEqual(course.price, 2000)
        self.assertEqual(course.is_accessible, True)
        self.assertEqual(len(course.professors.all()), 1)
        self.assertIn(self.professor, course.professors.all())

    def test_university(self):
        university = self.university
        self.assertEqual(university.name, "test")
        university.logo.open()
        self.assertEqual(university.logo.read(), self.content)
        university.logo.close()
        self.assertEqual(len(university.courses.all()), 1)
        self.assertIn(self.course, university.courses.all())
        self.assertEqual(len(university.majors.all()), 1)
        self.assertIn(self.major, university.majors.all())

    def test_university_image(self):
        university_image = self.university_image
        university_image.image.open()
        self.assertEqual(university_image.image.read(), self.content)
        university_image.image.close()
        self.assertEqual(university_image.university, self.university)

    def test_position(self):
        position = self.position
        self.assertEqual(position.title, "test")
        self.assertEqual(position.description, "test here")
        self.assertEqual(position.university, self.university)
        self.assertEqual(position.professor, self.professor)
        self.assertEqual(position.major, self.major)
        self.assertEqual(position.deadline, datetime.date.today())

    def test_education(self):
        education = self.education
        self.assertEqual(education.professor, self.professor)
        self.assertEqual(education.major, self.major)
        self.assertEqual(education.university, self.university)
        self.assertEqual(education.graduation_year, 2000)
