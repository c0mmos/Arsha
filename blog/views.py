from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.db.models import F, Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blog.forms import CommentForm
from django.contrib import messages

# Create your views here.

def blog_index(request, auth_username=None, cat_name=None, tag_name=None):
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())
    if auth_username:
        posts = posts.filter(author__username=auth_username)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if tag_name:
        posts = posts.filter(tag__name__in=[tag_name])
        
    posts = Paginator(posts, 4)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    context = {'posts': posts}

    return render(request, 'blog/blog-home.html', context)

def blog_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment submited successfully')
        else:
            messages.add_message(request, messages.ERROR, 'Your comment did not submited')
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())
    post = get_object_or_404(posts, pk=pid)
    comments = Comment.objects.filter(post=post.id, approved=True)

    Post.objects.filter(id=pid).update(counted_views=F('counted_views') + 1)

    previous_post = (
        posts
        .filter(published_date__lt=post.published_date)
        .order_by('-published_date')
        .first()
    )

    next_post = (
        posts
        .filter(published_date__gt=post.published_date)
        .order_by('published_date')
        .first()
    )

    form = CommentForm()

    context = {'post': post, 'previous_post': previous_post, 'next_post': next_post, 'comments': comments, 'form': form}
    post.refresh_from_db()

    return render(request, 'blog/blog-single.html', context=context)

@login_required
@require_POST
def like_comment(request, cid):
    comments = Comment.objects.filter(approved=True)
    comment = get_object_or_404(comments, pk=cid)

    if request.user in comment.like.all():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

def blog_search(request):
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())
    if request.method == 'GET':
        if s := request.GET.get('s'):
            posts = posts.filter(Q(title__icontains=s) | Q(content__contains=s))

    return render(request, 'blog/blog-home.html', {'posts': posts})
