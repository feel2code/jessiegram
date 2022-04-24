from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_slugs = ['test-slug1', 'test-slug2']
        cls.test_titles = ['Тестовая группа', 'Изменненная группа']
        cls.TEST_DESCRIPTION = 'Тестовое описание'
        cls.TEXT_LIMITATION = 15
        cls.test_users = ['HasNoName', 'Aboba']
        cls.test_texts = ['Тестовый пост', 'Тестовый пост 2']
        cls.test_verboses = {
            'group': 'Группа',
            'text': 'Текст поста',
            'author': 'Автор',
            'pub_date': 'Дата создания'}
        cls.test_labels = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'}
        cls.user = User.objects.create_user(username=cls.test_users[0])
        cls.group = Group.objects.create(
            title=cls.test_titles[0],
            slug=cls.test_slugs[0],
            description=cls.TEST_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=cls.test_texts[0],
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group_model = PostModelTest.group
        expected_object_name = group_model.title
        self.assertEqual(expected_object_name, str(group_model))

        post_model = PostModelTest.post
        expected_object_name = post_model.text[:PostModelTest.TEXT_LIMITATION]
        self.assertEqual(expected_object_name, str(post_model))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_verboses = {
            'group': PostModelTest.test_verboses['group'],
            'text': PostModelTest.test_verboses['text'],
            'author': PostModelTest.test_verboses['author'],
            'pub_date': PostModelTest.test_verboses['pub_date'],
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        task = PostModelTest.post
        field_help_texts = {
            'text': PostModelTest.test_labels['text'],
            'group': PostModelTest.test_labels['group'],
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).help_text, expected_value)
