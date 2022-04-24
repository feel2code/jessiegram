import shutil
import tempfile
from django.conf import settings
from http.client import OK
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Group, User, Comment


TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # testing variables
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
        cls.test_slugs = ['test-slug1', 'test-slug2']
        cls.post_ids = [25, 228]
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.test_texts = ['Тестовый пост', 'Измененный пост']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.object_status = {'not_created': 0, 'created': 1}
        cls.user = User.objects.create_user(username=cls.post_ids[1])
        cls.group = Group.objects.create(
            title=cls.test_titles[0],
            slug=cls.test_slugs[0],
            description=cls.TEST_DESCRIPTION,
        )
        cls.group2 = Group.objects.create(
            title=cls.test_titles[1],
            slug=cls.test_slugs[1],
            description=cls.TEST_DESCRIPTION,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        # guest client
        self.guest_client = Client()
        # auth client
        self.user = PostCreateFormTests.user
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_can_create_post(self):
        """проверка создания поста в БД и его изменение"""
        posts_count_before = Post.objects.count()
        form_data = {
            'text': PostCreateFormTests.test_texts[0],
            'group': PostCreateFormTests.group.id,
            'image': self.uploaded,
        }
        response1 = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post_id = str(response1.context['page_obj'].object_list[0].id)
        posts_count_after = Post.objects.count()
        self.assertEqual(response1.status_code, OK)
        self.assertEqual(
            posts_count_before,
            PostCreateFormTests.object_status['not_created']
        )
        self.assertEqual(
            posts_count_after,
            PostCreateFormTests.object_status['created']
        )

        # checking is post edited
        form_data = {
            'text': PostCreateFormTests.test_texts[1],
            'group': PostCreateFormTests.group2.id,
        }
        response2 = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                args=(post_id)
            ),
            data=form_data,
            follow=True
        )
        post = Post.objects.select_related('group').filter(id=post_id)
        self.assertEqual(
            response2.context['post'].text,
            post.values('text')[0]['text']
        )
        self.assertEqual(
            response2.context['post'].group.id,
            post.values('group_id')[0]['group_id']
        )

    def test_guest_cant_create_post(self):
        """проверка создания поста в БД гостем"""
        posts_count_before = Post.objects.count()
        form_data = {
            'text': PostCreateFormTests.test_texts[0],
            'group': PostCreateFormTests.group.id,
            'image': self.uploaded,
        }
        response1 = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        posts_count_after = Post.objects.count()
        self.assertEqual(response1.status_code, OK)
        self.assertEqual(
            posts_count_before,
            PostCreateFormTests.object_status['not_created']
        )
        self.assertNotEqual(
            posts_count_after,
            PostCreateFormTests.object_status['created']
        )

    def test_guest_cant_edit_post(self):
        """проверка создания поста в БД и его изменение гостем"""
        posts_count_before = Post.objects.count()
        Post.objects.create(
            author=self.user,
            text=self.test_texts[0],
            id=self.post_ids[0],
            image=self.uploaded,
            group=self.group
        )
        posts_count_after = Post.objects.count()
        post_id = Post.objects.latest('id').id
        self.assertEqual(
            posts_count_before,
            PostCreateFormTests.object_status['not_created']
        )
        self.assertEqual(
            posts_count_after,
            PostCreateFormTests.object_status['created']
        )

        # checking is post edited
        form_data = {
            'text': PostCreateFormTests.test_texts[1],
            'group': PostCreateFormTests.group2.id,
        }
        self.guest_client.post(
            reverse(
                'posts:post_edit',
                args=([post_id])
            ),
            data=form_data,
            follow=True
        )
        post = Post.objects.select_related('group').filter(id=post_id)
        group_name = (
            Group.objects.filter(
                id=post.values(
                    'group_id'
                )[0]['group_id']
            ).values('title')[0]['title']
        )
        self.assertNotEqual(
            PostCreateFormTests.test_texts[1],
            post.values('text')[0]['text']
        )
        self.assertNotEqual(
            PostCreateFormTests.test_titles[1],
            group_name
        )

    def test_authorized_can_comment(self):
        """Проверка создания комментария юзером"""
        post = Post.objects.create(
            text=PostCreateFormTests.test_texts[0],
            author=PostCreateFormTests.user,
            group=PostCreateFormTests.group
        )
        form_data = {
            'text': PostCreateFormTests.test_texts[0],
            'author': PostCreateFormTests.user.username,
            'post': post.id
        }
        count_before = Comment.objects.count()
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={
                    'post_id': post.id
                }),
            data=form_data,
            follow=True
        )
        new_comment = response.context['comments']
        count_after = Comment.objects.count()
        self.assertEqual(new_comment[0].text, form_data['text'])
        self.assertNotEqual(count_before, count_after)

        response1 = (
            self.authorized_client.get(
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': post.id}
                )
            )
        )
        comment_exist_text = response1.context['comments'][0].text
        self.assertEqual(comment_exist_text, PostCreateFormTests.test_texts[0])

    def test_guest_can_comment(self):
        """Проверка создания комментария гостем"""
        post = Post.objects.create(
            text=PostCreateFormTests.test_texts[0],
            author=PostCreateFormTests.user,
            group=PostCreateFormTests.group
        )
        form_data = {
            'text': PostCreateFormTests.test_texts[0],
            'author': PostCreateFormTests.user.username,
            'post': post.id
        }
        count_before = Comment.objects.count()
        self.guest_client.post(
            reverse(
                'posts:add_comment',
                kwargs={
                    'post_id': post.id
                }),
            data=form_data,
            follow=True
        )
        count_after = Comment.objects.count()
        self.assertEqual(count_before, count_after)
