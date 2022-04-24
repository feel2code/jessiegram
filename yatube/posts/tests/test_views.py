import shutil
import tempfile
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache


from ..forms import forms
from ..models import Post, Group, User, Follow


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
        cls.cached_reverse = 'posts:index'
        cls.test_post_html = {
            'create': 'posts/create_post.html',
            'edit': 'posts/create_post.html'}
        cls.test_slugs = ['test-slug', 'test-slug1', 'test-slug2']
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_description = 'Тестовое описание'
        cls.test_users = ['HasNoName', 'Aboba']
        cls.post_ids = [25, 228, 100500, 229, 230]
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.post_exist = {'yes': 'Естьпост', 'no': 'Нетпоста'}
        cls.TEST_PAGE_OBJ = '<Page 1 of 1>'
        cls.pages_limits = {'first': 10, 'second': 3}
        cls.test_post_count = [1, 2, 3]
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.user = User.objects.create_user(username=cls.test_users[1])
        cls.group = Group.objects.create(
            title=cls.test_titles[0],
            slug=cls.test_slugs[0],
            description=cls.TEST_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=cls.test_texts[0],
            id=cls.post_ids[1],
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text=cls.test_texts[1],
            id=cls.post_ids[3],
        )
        cls.post3 = Post.objects.create(
            author=cls.user,
            text=cls.test_texts[1],
            id=cls.post_ids[4],
            image=cls.uploaded,
            group=cls.group
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = PostsPagesTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'posts/index.html': (
                reverse('posts:index')
            ),
            'posts/group_list.html': (
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.test_slugs[0]})
            ),
            'posts/profile.html': (
                reverse(
                    'posts:profile',
                    kwargs={'username': self.test_users[1]})
            ),
            'posts/post_detail.html': (
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': str(self.post_ids[1])}
                )
            ),
            self.test_post_html['create']: (
                reverse('posts:post_create')
            ),
            self.test_post_html['edit']: (
                reverse(
                    'posts:post_edit',
                    kwargs={'post_id': str(self.post_ids[1])}
                )
            )
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:index',
                )
            )
        )
        check_obj = str(response.context['page_obj'])
        self.assertEqual(check_obj, self.TEST_PAGE_OBJ)

    def test_group_posts_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.test_slugs[0]}
                )
            )
        )
        check_obj = str(response.context['page_obj'])
        check_title = response.context.get('group').title
        check_slug = str(response.context.get('request')).replace(
            "<WSGIRequest: GET '", "").replace("'>", "")
        self.assertEqual(check_title, self.test_titles[0])
        self.assertEqual(check_slug, '/group/test-slug/')
        self.assertEqual(check_obj, self.TEST_PAGE_OBJ)

    def test_profile_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': self.test_users[1]}
                )
            )
        )
        check_obj = str(response.context['page_obj'])
        check_user = response.context.get('user').username
        check_count = response.context.get('post_count')
        self.assertEqual(check_user, self.test_users[1])
        self.assertEqual(check_obj, self.TEST_PAGE_OBJ)
        self.assertEqual(check_count, self.test_post_count[2])

    def test_post_detail_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': str(self.post_ids[1])}
                )
            )
        )
        check_user = response.context.get('user').username
        check_post = response.context.get('post').text
        check_id = response.context.get('post_id')
        author_posts_count = response.context.get('post').author.posts.count()
        self.assertEqual(check_user, self.test_users[1])
        self.assertEqual(check_post, self.test_texts[0])
        self.assertEqual(check_id, self.post.id)
        self.assertEqual(
            author_posts_count, self.test_post_count[2])

    def test_post_create_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:post_create'
                )
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_create_edit_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:post_edit',
                    kwargs={'post_id': self.post_ids[1]}
                )
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_index_image_context_correct(self):
        """Тест на наличие изображения в index"""
        response = (
            self.authorized_client.get(reverse('posts:index'))
        )
        test_image = response.context['page_obj'].object_list[0].image
        self.assertEqual(test_image, self.post3.image)

        response = (
            self.guest_client.get(reverse('posts:index'))
        )
        test_image = response.context['page_obj'].object_list[0].image
        self.assertEqual(test_image, self.post3.image)

    def test_profile_image_context_correct(self):
        """Тест на наличие изображения в profile"""
        response = (
            self.authorized_client.get(reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))
        )
        test_image = response.context['page_obj'].object_list[0].image
        self.assertEqual(test_image, self.post3.image)
        response = (
            self.guest_client.get(reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))
        )
        test_image = response.context['page_obj'].object_list[0].image
        self.assertEqual(test_image, self.post3.image)

    def test_post_with_image_context_correct(self):
        """Тест на наличие изображения в post_detail"""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={
                'post_id': self.post_ids[4]
            }
        ))
        test_image = response.context['post'].image
        self.assertEqual(test_image, self.post3.image)

    def test_group_post_with_image_context_correct(self):
        """Тест на наличие изображения в group_list"""
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': self.group.slug}))
        test_image = response.context['page_obj'].object_list[0].image
        self.assertEqual(test_image, self.post3.image)

    def test_cache(self):
        """Тест кэша"""
        first_response = self.guest_client.get(
            reverse(self.cached_reverse))
        post_cached = Post.objects.create(
            text=self.test_texts[0],
            author=self.user
        )
        response_not_cached = self.guest_client.get(
            reverse(self.cached_reverse))
        Post.objects.filter(id=post_cached.id).delete()
        response_cached = self.guest_client.get(
            reverse(self.cached_reverse))
        self.assertEqual(
            response_not_cached.content,
            response_cached.content
        )
        cache.delete('index_page')
        last_response = self.guest_client.get(
            reverse(self.cached_reverse))
        self.assertEqual(
            first_response.content,
            last_response.content
        )


class PaginatorViewsTest(TestCase):
    '''paginator's pages number test'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
        cls.test_post_html = {
            'create': 'posts/create_post.html',
            'edit': 'posts/create_post.html'}
        cls.test_slugs = ['test-slug', 'test-slug1', 'test-slug2']
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_description = 'Тестовое описание'
        cls.test_users = ['HasNoName', 'Aboba']
        cls.post_ids = [25, 228, 100500, 229]
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.post_exist = {'yes': 'Естьпост', 'no': 'Нетпоста'}
        cls.TEST_PAGE_OBJ = '<Page 1 of 1>'
        cls.pages_limits = {'first': 10, 'second': 3}
        cls.pages_url = ['', '?page=2']
        cls.user = User.objects.create_user(username=cls.test_users[1])
        cls.group = Group.objects.create(
            title=cls.test_titles[0],
            slug=cls.test_slugs[0],
            description=cls.TEST_DESCRIPTION,
        )

    def setUp(self):
        self.user = PaginatorViewsTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        for i in range(1, 14):
            PaginatorViewsTest.post = Post.objects.create(
                author=PaginatorViewsTest.user,
                group=PaginatorViewsTest.group,
                text=PaginatorViewsTest.test_texts[0] + str(i),
                id=i
            )

        page_count1 = self.client.get(
            reverse('posts:index')).context['page_obj'].end_index()
        self.assertEqual(
            page_count1,
            PaginatorViewsTest.pages_limits['first']
        )

        page_count2 = self.client.get(
            reverse('posts:index') + '?page=2').context['page_obj'].end_index()
        self.assertEqual(
            page_count2 - page_count1,
            PaginatorViewsTest.pages_limits['second']
        )

        group_page_count1 = (
            self.client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.test_slugs[0]}
                )
            ).context['page_obj'].end_index()
        )
        self.assertEqual(
            group_page_count1,
            PaginatorViewsTest.pages_limits['first']
        )

        group_page_count2 = (
            self.client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': PaginatorViewsTest.test_slugs[0]}
                ) + '?page=2'
            ).context['page_obj'].end_index()
        )
        self.assertEqual(
            group_page_count2 - group_page_count1,
            PaginatorViewsTest.pages_limits['second']
        )

        profile_page_count1 = (
            self.client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': PaginatorViewsTest.test_users[1]}
                )
            ).context['page_obj'].end_index()
        )
        self.assertEqual(
            profile_page_count1,
            PaginatorViewsTest.pages_limits['first']
        )

        profile_page_count2 = (
            self.client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': PaginatorViewsTest.test_users[1]}
                ) + PaginatorViewsTest.pages_url[1]
            ).context['page_obj'].end_index()
        )
        self.assertEqual(
            profile_page_count2 - profile_page_count1,
            PaginatorViewsTest.pages_limits['second']
        )


class AddViewTest(TestCase):
    '''additional creation post test'''
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
        cls.test_post_html = {
            'create': 'posts/create_post.html',
            'edit': 'posts/create_post.html'}
        cls.test_slugs = ['test-slug', 'test-slug1', 'test-slug2']
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_description = 'Тестовое описание'
        cls.test_users = ['HasNoName', 'Aboba']
        cls.post_ids = [25, 228, 100500, 229]
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.post_exist = {'yes': 'Естьпост', 'no': 'Нетпоста'}
        cls.TEST_PAGE_OBJ = '<Page 1 of 1>'
        cls.pages_limits = {'first': 10, 'second': 3}
        cls.user = User.objects.create_user(username=cls.test_users[1])
        cls.group1 = Group.objects.create(
            title=cls.post_exist['yes'],
            slug=cls.test_slugs[1],
            description=cls.TEST_DESCRIPTION,
        )
        cls.group2 = Group.objects.create(
            title=cls.post_exist['no'],
            slug=cls.test_slugs[2],
            description=cls.TEST_DESCRIPTION,
        )

    def setUp(self):
        self.user = AddViewTest.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        AddViewTest.post = Post.objects.create(
            author=AddViewTest.user,
            group=AddViewTest.group1,
            text=AddViewTest.test_texts[0],
            id=AddViewTest.post_ids[2]
        )
        response = self.authorized_client.get(reverse('posts:index'))
        check_index = response.context['page_obj'].object_list[0]
        self.assertEqual(str(check_index), AddViewTest.test_texts[0])

        response = (
            self.authorized_client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': AddViewTest.test_slugs[1]}
                )
            )
        )
        check_group = response.context['page_obj'].object_list[0]
        self.assertEqual(str(check_group), AddViewTest.test_texts[0])

        response = (
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': AddViewTest.test_users[1]}
                )
            )
        )
        check_profile = response.context['page_obj'].object_list[0]
        self.assertEqual(str(check_profile), AddViewTest.test_texts[0])

        response = (
            self.authorized_client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': AddViewTest.test_slugs[2]}
                )
            )
        )
        with self.assertRaises(IndexError):
            response.context['page_obj'].object_list[0]


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
        cls.follow_src = {
            'index': 'posts:follow_index',
            'follow': 'posts:profile_follow',
            'unfollow': 'posts:profile_unfollow'
        }
        cls.test_post_html = {
            'create': 'posts/create_post.html',
            'edit': 'posts/create_post.html'}
        cls.test_slugs = ['test-slug', 'test-slug1', 'test-slug2']
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_description = 'Тестовое описание'
        cls.test_users = ['HasNoName', 'Aboba', 'testovich']
        cls.post_ids = [25, 228, 100500, 229, 230]
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.post_exist = {'yes': 'Естьпост', 'no': 'Нетпоста'}
        cls.TEST_PAGE_OBJ = '<Page 1 of 1>'
        cls.pages_limits = {'first': 10, 'second': 3}
        cls.test_post_count = [1, 2, 3]
        cls.exists = {
            'yes': 1,
            'no': 0
        }
        cls.user1 = User.objects.create_user(username=cls.test_users[0])
        cls.user2 = User.objects.create_user(username=cls.test_users[1])
        cls.post1 = Post.objects.create(
            author=cls.user1,
            text=cls.test_texts[0],
            id=cls.post_ids[0],
        )
        cls.post2 = Post.objects.create(
            author=cls.user2,
            text=cls.test_texts[1],
            id=cls.post_ids[1],
        )

    def setUp(self):
        self.user1 = FollowTests.user1
        self.user2 = FollowTests.user2
        self.authorized_client1 = Client()
        self.authorized_client2 = Client()
        self.authorized_client1.force_login(self.user1)
        self.authorized_client2.force_login(self.user2)

    def test_auth_client_can_follow(self):
        """Юзер может фолловить"""
        follow_objects_before_follow = Follow.objects.filter(
            user=self.user1,
            author=self.user2
        ).count()
        self.authorized_client1.get(
            reverse(
                self.follow_src['follow'],
                kwargs={'username': self.user2.username}
            )
        )
        follow_objects_after_follow = Follow.objects.filter(
            user=self.user1,
            author=self.user2
        ).count()
        self.assertNotEqual(
            follow_objects_before_follow,
            follow_objects_after_follow
        )

    def test_auth_client_can_unfollow(self):
        """Юзер может отписаться"""
        self.authorized_client1.get(
            reverse(
                self.follow_src['follow'],
                kwargs={'username': self.user2.username}
            )
        )
        follow_objects_before_unfollow = Follow.objects.filter(
            user=self.user1,
            author=self.user2
        ).count()
        self.authorized_client1.get(
            reverse(
                self.follow_src['unfollow'],
                kwargs={'username': self.user2.username}
            )
        )
        follow_objects_after_unfollow = Follow.objects.filter(
            user=self.user1,
            author=self.user2
        ).count()
        self.assertNotEqual(
            follow_objects_before_unfollow,
            follow_objects_after_unfollow
        )

    def test_auth_clients_follow(self):
        """Проверка подписок разных юзеров"""
        self.authorized_client1.get(
            reverse(
                self.follow_src['follow'],
                kwargs={'username': self.user2.username}
            )
        )
        response_user1 = (
            self.authorized_client1.get(reverse(self.follow_src['index']))
        )
        self.assertEqual(
            response_user1.context['page_obj'].object_list[0],
            self.post2
        )
        count_of_followings = (
            self.authorized_client2.get(reverse(self.follow_src['index']))
        ).context.get('post')
        self.assertIsNone(count_of_followings)
