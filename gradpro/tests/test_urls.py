from django.test import TestCase
from django.urls import reverse

class UrlTest(TestCase):
    def test_about_url(self):
        response = self.client.get('/gradpro/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_url_reverse(self):
        response = self.client.get(reverse('gradpro:about'))
        self.assertEqual(response.status_code, 200)

    def test_index_url(self):
        response = self.client.get('/gradpro/')
        self.assertEqual(response.status_code, 200)

    def test_index_url_reverse(self):
        response = self.client.get(reverse('gradpro:index'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get('/gradpro/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_reverse(self):
        response = self.client.get(reverse('gradpro:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        response = self.client.get('/gradpro/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_url_reverse(self):
        response = self.client.get(reverse('gradpro:login'))
        self.assertEqual(response.status_code, 200)
