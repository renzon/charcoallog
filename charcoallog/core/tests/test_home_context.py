from django.contrib.auth.models import User
from django.test import TestCase

from charcoallog.core.service import ShowData


class HomeContextTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='teste')
        user.set_password('1qa2ws3ed')
        user.save()

        self.login_in = self.client.login(username='teste', password='1qa2ws3ed')
        self.response = self.client.get('/')

    def test_status_code(self):
        """ status code must be 200 """
        self.assertEqual(200, self.response.status_code)

    def test_context_only_instance(self):
        show_data = self.response.context['show_data']
        self.assertIsInstance(show_data, ShowData)

    def test_logout_link(self):
        self.assertContains(self.response, '<a href')

    def test_html_register_forms(self):
        """" Html must contain input tags """
        tags = (
            ('<form', 2),
            ('<input', 9),
            ('<select', 6),
            ('type="text"', 5),
            # ('type="hidden"', 3),
            ('<button', 2),
            ('type=\'submit\'', 2)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """" must have csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_bottom_id(self):
        self.assertContains(self.response, '<b>charcoallog released under GPL-3+</b>')
