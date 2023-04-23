from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


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
        verbose_name=_("Post text"),
        help_text=_("Enter post's text")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Author')
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group',
        blank=True,
        null=True,
        verbose_name=_('Group'),
        help_text=_('Related group')
    )
    pub_date = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        db_index=True
    )
    image = models.ImageField(
        _('Photo'),
        upload_to='posts/',
    )
    like = models.BooleanField(
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Comment(models.Model):
    def __str__(self):
        return None or ''

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Comment'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Author'),
    )
    text = models.CharField(
        max_length=200,
        help_text=_("Enter post's text"),
    )
    pub_date = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        db_index=True
    )


class Follow(models.Model):
    def __str__(self):
        return f'{self.user.username} follows {self.author.username}' or ''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name=_('Follower'),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Following'),
    )
    pub_date = models.DateTimeField(
        _('Created at'),
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
