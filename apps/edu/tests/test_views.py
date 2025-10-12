from django.test import TestCase
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.edu.views import (
    PositionListView, PositionDetailView
)
from apps.edu.models import (
    Position
)


class PositionListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position_list_url = reverse('edu:position-list')

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


class PositionListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position_detail_url = reverse('edu:position-detail', kwargs=)

    def setUp(self):
        self.response = self.client.get(self.position_detail_url)
    
    def test_position_detail_accessible(self):
        self.assertEqual(self.response.status_code, 200)

    def test_position_detail_template(self):
        self.assertTemplateUsed(self.response, "home/position_detail.html")

    def test_position_detail_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_position_detail_url_resolves_position_detail_view(self):
        view = resolve(self.position_detail_url)
        self.assertEqual(view.func.view_class, PositionDetailView)