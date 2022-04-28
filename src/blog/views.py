from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from .models import Post
from .forms import PostForm


# Group.objects.get_or_create(name='Subscriber')
# Group.objects.get_or_create(name='Author')


def post_list(request):
    current_user = request.user
    group = current_user.groups.first()

    if current_user.groups.filter(name='Subscriber').exists():
        posts = Post.objects.all().order_by('created_date')
    elif current_user.groups.filter(name='Author').exists():
        posts = Post.objects.filter(Q(public=True) | Q(author=current_user)) \
            .order_by('created_date')
    else:
        posts = Post.objects.filter(public=True).order_by('created_date')

    return render(request, 'blog/post_list.html',
                  {'posts': posts, 'current_user': current_user,
                   'group': group})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


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
