from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Post, Like, Dislike, Subscription
from .forms import PostForm


def post_list(request):
    current_user = request.user
    group = current_user.groups.first()

    # Author does not have subscriber rights
    # if current_user.groups.filter(name='Subscriber').exists():
    #     posts = Post.objects.all().order_by('created_date')
    # elif current_user.groups.filter(name='Author').exists():
    #     posts = Post.objects.filter(Q(public=True) | Q(author=current_user)) \
    #         .order_by('created_date')
    # else:
    #     posts = Post.objects.filter(public=True).order_by('created_date')

    # Author has subscriber rights
    if current_user.groups.filter(Q(name='Subscriber') | Q(name='Author'))\
            .exists():
        posts = Post.objects.all().order_by('created_date')
    else:
        posts = Post.objects.filter(public=True).order_by('created_date')

    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'group': group})


@login_required
def subscriptions_list(request):
    posts = Post.objects.filter(author__subscriber_id__subscriber=request.user)

    return render(request, 'blog/subscriptions_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_authenticated and not post.public:
        raise PermissionDenied()

    return render(request, 'blog/post_detail.html', {'post': post})


def user_detail(request, username):
    second_user = User.objects.get(username=username)
    posts = Post.objects.filter(author=second_user)
    count_posts = second_user.posts_id.count()
    if request.user.is_authenticated:
        sub = Subscription.objects.filter(subscriber=request.user,
                                          subscribed=second_user).exists()
    else:
        sub = None

    return render(request, 'blog/user_page.html',
                  {'second_user': second_user,
                   'sub': sub, 'posts': posts, 'count_posts': count_posts})


@login_required
def post_new(request):
    current_user = request.user

    if not current_user.groups.filter(name='Author').exists():
        raise PermissionDenied()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = current_user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied()

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        raise PermissionDenied()

    post.delete()
    return redirect('post_list')


@login_required
def add_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user

    try:
        Like.objects.get(author=current_user, post=post).delete()
    except Like.DoesNotExist:
        Like.objects.create(author=current_user, post=post)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user

    try:
        Dislike.objects.get(author=current_user, post=post).delete()
    except Dislike.DoesNotExist:
        Dislike.objects.create(author=current_user, post=post)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def subscribe(request, pk):
    current_user = request.user
    post_author = User.objects.get(pk=pk)

    try:
        Subscription.objects.get(subscriber=current_user,
                                 subscribed=post_author).delete()
    except Subscription.DoesNotExist:
        Subscription.objects.create(subscriber=current_user,
                                    subscribed=post_author)

    return redirect(request.META.get('HTTP_REFERER'))
