from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'qwerty'
        password = 'haslo123'
        User.objects.create_user(username=username, email='aaa@aaa.com', password=password)
        url = reverse('password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)