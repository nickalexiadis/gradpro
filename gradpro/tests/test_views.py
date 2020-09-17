from gradpro.models import User
from django.urls import reverse
from django.test.client import Client
from django.test import TestCase


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('nick@a.com', 'password')

    def test_about(self):
        self.client.login(email='@a.com', password='password')
        response = self.client.get(reverse('gradpro:about'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_non_authenticated(self):
        response = self.client.get(reverse('gradpro:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard(self):
        self.client.login(email='nick@a.com', password='password')
        response = self.client.get(reverse('gradpro:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        self.client.login(email='nick@a.com', password='password')
        response = self.client.get(reverse('gradpro:index'))
        self.assertEqual(response.status_code, 200)

