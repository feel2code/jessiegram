from http.client import OK, FOUND, NOT_FOUND
from django.test import TestCase, Client

from ..models import Post, Group, User


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
        cls.test_post_html = {
            'create': 'posts/create_post.html',
            'edit': 'posts/create_post.html'}
        cls.test_slugs = ['test-slug1', 'test-slug2']
        cls.post_ids = [25, 228]
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_description = 'Тестовое описание'
        cls.test_users = ['HasNoName', 'Aboba']
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{cls.test_slugs[0]}/',
            'posts/profile.html': '/profile/HasNoName/',
            'posts/post_detail.html': f'/posts/{cls.post_ids[0]}/',
            cls.test_post_html['create']: '/create/',
            cls.test_post_html['edit']: f'/posts/{cls.post_ids[0]}/edit'
        }
        # status codes of url for authorized client
        cls.urls_auth = {
            '/': OK,
            f'/group/{cls.test_slugs[0]}/': OK,
            '/profile/HasNoName/': OK,
            f'/posts/{cls.post_ids[0]}/': OK,
            '/create/': OK,
            f'/posts/{cls.post_ids[0]}/edit': OK,
            f'/posts/{cls.post_ids[1]}/edit': FOUND,
            '/aboba': NOT_FOUND
        }
        # status codes of url for guest client
        cls.urls_guest = {
            '/': OK,
            f'/group/{cls.test_slugs[0]}/': OK,
            '/profile/HasNoName/': OK,
            f'/posts/{cls.post_ids[0]}/': OK,
            '/create/': FOUND,
            f'/posts/{cls.post_ids[0]}/edit': FOUND,
            f'/posts/{cls.post_ids[1]}/edit': FOUND,
            '/aboba': NOT_FOUND
        }
        cls.excepted_dict = {
            'post_id_edit': f'/posts/{cls.post_ids[1]}/edit',
            'post_id_redirect': f'/posts/{cls.post_ids[1]}/',
            'post_id_create': '/create/',
            'guest_create': '/auth/login/?next=/create/'
        }
        cls.user = User.objects.create_user(username=cls.test_users[0])
        cls.user2 = User.objects.create_user(username=cls.test_users[1])
        cls.group = Group.objects.create(
            title=cls.test_titles[0],
            slug=cls.test_slugs[0],
            description=cls.test_description,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=cls.test_texts[0],
            id=cls.post_ids[0]
        )
        # create post, which uneditable for user test_users[0]
        cls.post2 = Post.objects.create(
            author=cls.user2,
            text=cls.test_texts[1],
            id=cls.post_ids[1]
        )

    def setUp(self):
        # create guest client
        self.guest_client = Client()
        # create auth client
        self.user = PostsURLTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, address in PostsURLTests.templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """Проверка доступности адресов"""
        for address, status_code in PostsURLTests.urls_auth.items():
            with self.subTest(status_code=status_code):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, status_code)

        for address, status_code in PostsURLTests.urls_guest.items():
            with self.subTest(status_code=status_code):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, status_code)

    # checking redirects
    def test_create_url_redirect_anonymous_on_admin_login(self):
        """Страница создания поста перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get(
            PostsURLTests.excepted_dict['post_id_create'],
            follow=True
        )
        self.assertRedirects(
            response,
            PostsURLTests.excepted_dict['guest_create']
        )

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        """Страница изменения поста перенаправит
        авторизированного пользователя на страницу поста.
        """
        response = self.authorized_client.get(
            PostsURLTests.excepted_dict['post_id_edit'], follow=True
        )
        self.assertRedirects(
            response,
            PostsURLTests.excepted_dict['post_id_redirect']
        )
