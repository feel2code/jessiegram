from django.test import TestCase, Client
from django.urls import reverse
from http.client import OK


class StaticPagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.urls = {
            'author': '/about/author/',
            'tech': '/about/tech/'
        }
        self.htmls = {
            'author': 'about/author.html',
            'tech': 'about/tech.html',
        }

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адресов /about/~"""
        response = self.guest_client.get(self.urls['author'])
        self.assertEqual(response.status_code, OK)

        response = self.guest_client.get(self.urls['tech'])
        self.assertEqual(response.status_code, OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адресов /about/~"""
        response = self.guest_client.get(self.urls['author'])
        self.assertTemplateUsed(response, self.htmls['author'])

        response = self.guest_client.get(self.urls['tech'])
        self.assertTemplateUsed(response, self.htmls['tech'])


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.urls_reverse = {
            'author': 'about:author',
            'tech': 'about:tech'
        }
        self.htmls = {
            'author': 'about/author.html',
            'tech': 'about/tech.html',
        }

    def test_author_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:about, доступен."""
        response = self.guest_client.get(reverse(self.urls_reverse['author']))
        self.assertEqual(response.status_code, OK)

    def test_author_page_uses_correct_template(self):
        """При запросе к about:author
        применяется шаблон about/author.html."""
        response = self.guest_client.get(reverse(self.urls_reverse['author']))
        self.assertTemplateUsed(response, self.htmls['author'])

    def test_tech_page_accessible_by_name(self):
        """URL, генерируемый при помощи имени about:tech, доступен."""
        response = self.guest_client.get(reverse(self.urls_reverse['tech']))
        self.assertEqual(response.status_code, OK)

    def test_tech_page_uses_correct_template(self):
        """При запросе к about:tech
        применяется шаблон about/tech.html."""
        response = self.guest_client.get(reverse(self.urls_reverse['tech']))
        self.assertTemplateUsed(response, self.htmls['tech'])
