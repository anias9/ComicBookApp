from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class MyAccountTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = 'secret123'
        self.user = User.objects.create_user(username=self.username, email='aaa@aaaa.com', password=self.password)
        self.url = reverse('my_account')
