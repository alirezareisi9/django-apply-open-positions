import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.edu.views import (
    PositionListView,
    PositionDetailView,
    UniversityListView,
    ProfessorListView,
    CourseListView,
    PublicationListView,
    UniversityDetailView,
    ProfessorDetailView,
    CourseDetailView,
    PublicationDetailView,
)
from apps.edu.models import (
    Position,
    University,
    Professor,
    Major,
    Authorship,
    Course,
    Education,
    Teaching,
    UniversityCourse,
    UniversityImage,
    Publication,
    Field,
)


class PositionListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position_list_url = reverse("edu:position-list")

    def setUp(self):
        self.response = self.client.get(self.position_list_url)

    def test_position_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_position_list_template(self):
        self.assertTemplateUsed(self.response, "home/position_list.html")

    def test_position_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_position_list_url_resolves_position_list_view(self):
        view = resolve(self.position_list_url)
        self.assertEqual(view.func.view_class, PositionListView)


class UniversityListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.university_list_url = reverse("edu:university-list")

    def setUp(self):
        self.response = self.client.get(self.university_list_url)

    def test_university_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_university_list_template(self):
        self.assertTemplateUsed(self.response, "home/university_list.html")

    def test_university_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_university_list_url_resolves_university_list_view(self):
        view = resolve(self.university_list_url)
        self.assertEqual(view.func.view_class, UniversityListView)


class ProfessorListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.professor_list_url = reverse("edu:professor-list")

    def setUp(self):
        self.response = self.client.get(self.professor_list_url)

    def test_professor_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_professor_list_template(self):
        self.assertTemplateUsed(self.response, "home/professor_list.html")

    def test_professor_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_professor_list_url_resolves_professor_list_view(self):
        view = resolve(self.professor_list_url)
        self.assertEqual(view.func.view_class, ProfessorListView)


class CourseListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course_list_url = reverse("edu:course-list")

    def setUp(self):
        self.response = self.client.get(self.course_list_url)

    def test_course_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_course_list_template(self):
        self.assertTemplateUsed(self.response, "home/course_list.html")

    def test_course_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_course_list_url_resolves_course_list_view(self):
        view = resolve(self.course_list_url)
        self.assertEqual(view.func.view_class, CourseListView)


class PublicationListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.publication_list_url = reverse("edu:publication-list")

    def setUp(self):
        self.response = self.client.get(self.publication_list_url)

    def test_publication_list_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_publication_list_template(self):
        self.assertTemplateUsed(self.response, "home/publication_list.html")

    def test_publication_list_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_publication_list_url_resolves_publication_list_view(self):
        view = resolve(self.publication_list_url)
        self.assertEqual(view.func.view_class, PublicationListView)


class DetailViewsTests(TestCase):
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

        cls.position_url = reverse(
            "edu:position-detail", kwargs={"pk": cls.position.id}
        )
        cls.university_url = reverse(
            "edu:university-detail", kwargs={"pk": cls.university.id}
        )
        cls.professor_url = reverse(
            "edu:professor-detail", kwargs={"pk": cls.professor.id}
        )
        cls.course_url = reverse("edu:course-detail", kwargs={"pk": cls.course.id})
        cls.publication_url = reverse(
            "edu:publication-detail", kwargs={"pk": cls.publication.id}
        )

    def setUp(self):
        self.position_response = self.client.get(self.position_url)
        self.university_response = self.client.get(self.university_url)
        self.professor_response = self.client.get(self.professor_url)
        self.course_response = self.client.get(self.course_url)
        self.publication_response = self.client.get(self.publication_url)

    # position-detail
    def test_position_detail_accessible(self):
        self.assertEqual(self.position_response.status_code, 200)

    def test_position_detail_template(self):
        self.assertTemplateUsed(self.position_response, "home/position_detail.html")

    def test_position_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.position_response, "Hi there! I should not be on the page."
        )

    def test_position_detail_url_resolves_position_detail_view(self):
        view = resolve(self.position_url)
        self.assertEqual(view.func.view_class, PositionDetailView)

    # university-detail
    def test_university_detail_accessible(self):
        self.assertEqual(self.university_response.status_code, 200)

    def test_university_detail_template(self):
        self.assertTemplateUsed(self.university_response, "home/university_detail.html")

    def test_university_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.university_response, "Hi there! I should not be on the page."
        )

    def test_university_detail_url_resolves_university_detail_view(self):
        view = resolve(self.university_url)
        self.assertEqual(view.func.view_class, UniversityDetailView)

    # professor-detail
    def test_professor_detail_accessible(self):
        self.assertEqual(self.professor_response.status_code, 200)

    def test_professor_detail_template(self):
        self.assertTemplateUsed(self.professor_response, "home/professor_detail.html")

    def test_professor_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.professor_response, "Hi there! I should not be on the page."
        )

    def test_professor_detail_url_resolves_professor_detail_view(self):
        view = resolve(self.professor_url)
        self.assertEqual(view.func.view_class, ProfessorDetailView)

    # course-detail
    def test_course_detail_accessible(self):
        self.assertEqual(self.course_response.status_code, 200)

    def test_course_detail_template(self):
        self.assertTemplateUsed(self.course_response, "home/course_detail.html")

    def test_course_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.course_response, "Hi there! I should not be on the page."
        )

    def test_course_detail_url_resolves_course_detail_view(self):
        view = resolve(self.course_url)
        self.assertEqual(view.func.view_class, CourseDetailView)

    # publication-detail
    def test_publication_detail_accessible(self):
        self.assertEqual(self.publication_response.status_code, 200)

    def test_publication_detail_template(self):
        self.assertTemplateUsed(
            self.publication_response, "home/publication_detail.html"
        )

    def test_publication_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.publication_response, "Hi there! I should not be on the page."
        )

    def test_publication_detail_url_resolves_publication_detail_view(self):
        view = resolve(self.publication_url)
        self.assertEqual(view.func.view_class, PublicationDetailView)
