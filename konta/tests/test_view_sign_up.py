from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import SignUpForm
from ..views import rejestracja


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('rejestracja')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/rejestracja/')
        self.assertEquals(view.func, rejestracja)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


