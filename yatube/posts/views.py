from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Like, Post, Group, User, Follow
from .forms import PostForm, CommentForm, GroupForm
from .paginator import paginator_module


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.select_related(
        'group'
    ).order_by(
        '-pub_date'
    )
    context = {
        'page_obj': paginator_module(request, post_list),
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    post_list = Post.objects.select_related(
        'group'
    ).filter(
        group__title=group
    ).order_by(
        '-pub_date'
    )
    context = {
        'group': group,
        'page_obj': paginator_module(request, post_list),
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    following = False
    yourself = False
    # checking if client is authorized
    if request.user.is_authenticated:
        current_user = request.user
        # checking if client is following this author
        following = Follow.objects.filter(
            user=current_user,
            author=author
        )
        # checking if its clients profile
        if current_user == author:
            yourself = True

    post_list = Post.objects.select_related(
        'group', 'author'
    ).filter(
        author__username=username
    ).order_by(
        '-pub_date'
    )
    context = {
        'username': author,
        'page_obj': paginator_module(request, post_list),
        'post_count': post_list.count(),
        'following': following,
        'yourself': yourself
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    editable = False
    liked = False
    if request.user.is_authenticated:
        current_user = request.user
        liked = Like.objects.filter(user=current_user, post=post_id).exists()
        if current_user == post.author:
            editable = True
    post_count = post.author.posts.count()
    form = CommentForm()
    post_comments = post.comments.all()
    context = {
        'post_id': post_id,
        'post': post,
        'post_count': post_count,
        'form': form,
        'comments': post_comments,
        'editable': editable,
        'liked': liked,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    author = request.user
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        new_post = Post(
            text=form.cleaned_data['text'],
            author=author,
            group=form.cleaned_data['group'],
            image=form.cleaned_data['image']
        )
        new_post.save()
        return redirect(f'/profile/{author}/')
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def group_create(request):
    template = 'posts/create_group.html'
    form = GroupForm(
        request.POST or None,
    )
    if form.is_valid():
        new_group = Group(
            title=form.cleaned_data['title'],
            slug=form.cleaned_data['slug'],
            description=form.cleaned_data['description'],
        )
        new_group.save()
        return redirect('posts:index')
    context = {
        'form': form,
    }

    return render(request, template, context)


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    author = request.user
    if author == post.author:
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            post.save()
            return redirect(f'/posts/{post_id}/')
        context = {
            'form': form,
            'post': post,
            'is_edit': True
        }
        return render(request, template, context)
    return redirect(f'/posts/{post_id}/')


def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    current_user = request.user
    if current_user == post.author:
        print(dir(current_user))
        current_user.posts.filter(id=post_id).delete()
        return redirect('posts:profile', username=current_user.username)
    return redirect(f'/posts/{post_id}/')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    current_user = request.user
    post_list = Post.objects.select_related(
        'group', 'author'
    ).filter(
        author__following__user=current_user
    ).order_by(
        '-pub_date'
    )
    context = {
        'page_obj': paginator_module(request, post_list),
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    current_user = request.user
    if current_user != author and not (
        current_user.follower.filter(author=author).exists()
    ):
        current_user.follower.create(author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    current_user = request.user
    if current_user != author:
        current_user.follower.filter(author=author).delete()
    return redirect('posts:profile', username=username)


@login_required
def add_or_delete_like(request, post_id):
    current_user = request.user
    post = Post.objects.filter(id=post_id).get()
    liked = Like.objects.filter(user=current_user, post=post_id).exists()
    if not liked:
        Like.objects.create(user=current_user, post=post)
    else:
        Like.objects.filter(user=current_user, post=post).delete()
    return redirect(request.META.get('HTTP_REFERER'))
