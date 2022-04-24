from django import forms
from .models import Post, Comment, Group


class PostForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label='Введите текст',
        required=True,
        help_text='Текст поста'
    )

    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {'group': 'Выберите группу'}


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label='Введите текст',
        required=True,
        help_text='Текст поста'
    )

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Комментарий'}


class GroupForm(forms.ModelForm):
    title = forms.CharField(
        max_length=20,
        label='Введите текст',
        required=True,
        help_text='Название группы'
    )
    slug = forms.SlugField(
        max_length=15,
        label='Введите текст на латинице',
        required=True,
        help_text='Короткая ссылка'
    )
    description = forms.CharField(
        max_length=25,
        label='Введите текст',
        required=True,
        help_text='Описание группы'
    )

    class Meta:
        model = Group
        fields = ['title', 'slug', 'description']
