from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment, Group


class PostForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label=_("Enter post's text"),
        required=True,
        help_text=_("Post's text")
    )

    class Meta:
        model = Post
        fields = ['text', 'group', 'image']
        labels = {'group': _('Select group')}


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label=_("Enter post's text"),
        required=True,
        help_text=_("Post's text")
    )

    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': _('Comment')}


class GroupForm(forms.ModelForm):
    title = forms.CharField(
        max_length=20,
        label=_("Enter text"),
        required=True,
        help_text=_("Name of the group")
    )
    slug = forms.SlugField(
        max_length=15,
        label=_("Enter text with latin symbols"),
        required=True,
        help_text=_("Short link")
    )
    description = forms.CharField(
        max_length=25,
        label=_("Enter text"),
        required=True,
        help_text=_("Description of the group")
    )

    class Meta:
        model = Group
        fields = ['title', 'slug', 'description']
