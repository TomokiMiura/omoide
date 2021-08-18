from django.test import TestCase
from django.urls import reverse, resolve
from ..views import SearchResultView

class TestUrls(TestCase):

    def test_search_url(self):
        view = resolve('/search/')
        self.assertEqual(view.func.view_class, SearchResultView)