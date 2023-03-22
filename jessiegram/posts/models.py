from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    def __str__(self):
        return self.title or ''

    title = models.CharField(
        max_length=20
    )
    slug = models.SlugField(
        unique=True
    )
    description = models.CharField(
        max_length=25
    )


class Post(models.Model):
    def __str__(self):
        return self.text[:15] or ''

    text = models.CharField(
        max_length=200,
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
    )
    like = models.BooleanField(
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    def __str__(self):
        return None or ''

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.CharField(
        max_length=200,
        help_text='Впишите текст здесь',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )


class Follow(models.Model):
    def __str__(self):
        return f'{self.user.username}подписан на {self.author.username}' or ''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )


class Like(models.Model):
    def __str__(self):
        return f'{self.user}'

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_like',
    )
