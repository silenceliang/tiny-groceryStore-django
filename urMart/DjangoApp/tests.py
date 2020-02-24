from django.test import TestCase
from django.urls import resolve
from .views import BackendView
# Create your tests here.

class TestBackendView(TestCase):
    def test_resolve_to_backend(self):
        found = resolve('/')
        # check function name is equal 
        self.assertEqual(found.func.__name__, BackendView.as_view().__name__)
    def test_render_to_backend(self):
        response = self.client.get('/')
        # check which template is used
        self.assertTemplateUsed(response, 'index.html')
        # check response status is equal to 200
        self.assertEqual(response.status_code, 200)