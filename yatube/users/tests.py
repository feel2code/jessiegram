from http.client import NOT_FOUND, OK, FOUND
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='HasNoName', password='aboba'
        )

    def setUp(self):
        # create guest client
        self.guest_client = Client()
        # create auth client
        self.user = UsersURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/<uidb64>/<token>/': (
                'users/password_reset_confirm.html'),
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

        templates_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/<uidb64>/<token>/': (
                'users/password_reset_confirm.html'),
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """Проверка доступности адресов"""
        # test for authorized client
        urls = {
            '/auth/signup/': OK,
            '/auth/login/': OK,
            '/auth/password_change/': OK,
            '/auth/password_change/done/': OK,
            '/auth/password_reset/': OK,
            '/auth/reset/<uidb64>/<token>/': OK,
            '/auth/reset/done/': OK,
            '/auth/logout/': OK,
            '/auth/random': NOT_FOUND
        }
        for address, status_code in urls.items():
            with self.subTest(status_code=status_code):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status_code)

        # test for guest client
        urls = {
            '/auth/signup/': OK,
            '/auth/login/': OK,
            '/auth/password_change/': FOUND,
            '/auth/password_change/done/': FOUND,
            '/auth/password_reset/': OK,
            '/auth/reset/<uidb64>/<token>/': OK,
            '/auth/reset/done/': OK,
            '/auth/logout/': OK,
            '/auth/random': NOT_FOUND
        }
        for address, status_code in urls.items():
            with self.subTest(status_code=status_code):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    # checking redirects
    def test_login_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу изменения пароля перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/auth/password_change/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/'
        )

        response = self.guest_client.get(
            '/auth/password_change/done/', follow=True
        )
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/done/'
        )

        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )


class StaticViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Aboba')

    def setUp(self):
        self.guest_client = Client()
        self.user = StaticViewsTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_pages_accessible_by_name(self):
        """шаблны, указанные при помощи имен users, доступны."""
        templates_namespaces = {
            'users:signup': 'users/signup.html',
            'users:login': 'users/login.html',
            'users:password_change': 'users/password_change_form.html',
            'users:password_change_done': 'users/password_change_done.html',
            'users:password_reset': 'users/password_reset_form.html',
            'users:password_reset_done': 'users/password_reset_done.html',
            'users:password_reset_complete': (
                'users/password_reset_complete.html'),
            'users:logout': 'users/logged_out.html',
        }
        for address, template in templates_namespaces.items():
            with self.subTest(address=address):
                response = self.guest_client.get(reverse(address))
                self.assertTemplateUsed(response, template)

        for address, template in templates_namespaces.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(reverse(address))
                self.assertTemplateUsed(response, template)

    def test_pass_confirm_uses_correct_template(self):
        """При запросе к users:password_reset_confirm
        применяется шаблон users/password_reset_confirm.html."""
        response_guest = self.guest_client.get(
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': '<uidb64>',
                        'token': '<token>'}
            )
        )
        response_auth = self.authorized_client.get(
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': '<uidb64>',
                        'token': '<token>'}
            )
        )
        self.assertTemplateUsed(
            response_guest, 'users/password_reset_confirm.html')
        self.assertTemplateUsed(
            response_auth, 'users/password_reset_confirm.html')

    def test_users_pages_accessible_by_name(self):
        """URL, генерируемые при помощи имен users, доступны."""
        names = {
            'users:signup': OK,
            'users:login': OK,
            'users:password_change': OK,
            'users:password_change_done': OK,
            'users:password_reset': OK,
            'users:password_reset_done': OK,
            'users:password_reset_complete': OK,
            'users:logout': OK,
        }
        for address, status_code in names.items():
            with self.subTest(status_code=status_code):
                response = self.authorized_client.get(reverse(address))
                self.assertEqual(response.status_code, status_code)

        # test for guest client
        names = {
            'users:signup': OK,
            'users:login': OK,
            'users:password_change': FOUND,
            'users:password_change_done': FOUND,
            'users:password_reset': OK,
            'users:password_reset_done': OK,
            'users:password_reset_complete': OK,
            'users:logout': OK,
        }
        for address, status_code in names.items():
            with self.subTest(status_code=status_code):
                response = self.guest_client.get(reverse(address))
                self.assertEqual(response.status_code, status_code)

    def test_signup_correct_context(self):
        """Шаблон signup для юзера сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_signup_guest_correct_context(self):
        """Шаблон signup для гостя сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('users:signup'))
        form_fields = {
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class UsersFormsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_new_user(self):
        """тест на создание юзера и на редирект на главную"""
        users_count_before = User.objects.count()
        form_data = {
            'first_name': 'Abobov',
            'last_name': 'Abobov',
            'username': 'abobov',
            'email': 'aboba@mail.ru',
            'password1': 'Asboba123!',
            'password2': 'Asboba123!'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        users_count_after = User.objects.count()
        self.assertEqual(users_count_before, 0)
        self.assertEqual(users_count_after, 1)
        self.assertRedirects(response, '/')
