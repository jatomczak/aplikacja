from django.test import TestCase
from django.http import HttpRequest

from okbv import views
from okbv import forms

class OkbvViews(TestCase):

    def setUp(self):
        pass

    def test_home(self):
        request = HttpRequest()
        response = views.home(request)
        self.assertEqual(response.content, b'test')

    def test_upload_file_GET(self):
        request = HttpRequest()
        request.method = 'GET'
        form = forms.UploadFileForm()
        response = views.upload_file(request)
        self.assertIn(bytes(form.as_p(), 'utf-8'), response.content)


