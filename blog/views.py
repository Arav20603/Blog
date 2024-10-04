from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import PostForm, CommentForm, CategoryForm, TagForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

# Create your views here.
@login_required
@permission_required('blog.add_post', raise_exception=True)
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_list_view(request):
    query = request.GET.get('q')  # Get the search query from the request
    post_list = Post.objects.all().order_by('created_at')

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )  # Search in both title and content fields

    paginator = Paginator(post_list, 2) # Show 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'query': query or ''})

@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form,})

@login_required
@permission_required('blog.change_post', raise_exception=True)
def post_update_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user and not request.user.has_perm('blog.change_post'):
        raise PermissionDenied()  # Prevent users from editing posts they don't own
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
@permission_required('blog.delete_post', raise_exception=True)
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user and not request.user.has_perm('blog.delete_post'):
        raise PermissionDenied()  # Prevent users from deleting others' posts without permission

    # if request.method == 'POST':
    #     post.delete()
    #     return redirect('post_list')
    # return render(request, 'blog/post_confirm_delete.html', {'post': post})
    post.delete()
    return redirect('post_list')

@login_required
def category_user_view(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.save()
            return redirect('post_create')
    else:
        category_form = CategoryForm()
    return render(request, 'blog/category_new.html', {'category_form': category_form})

@login_required
def tag_user_view(request):
    if request.method == 'POST':
        tag_form = TagForm(request.POST)
        if tag_form.is_valid():
            tag = tag_form.save(commit=False)
            tag.save()
            return redirect('post_create')
    else:
        tag_form = TagForm()
    return render(request, 'blog/tag_new.html', {'tag_form': tag_form})