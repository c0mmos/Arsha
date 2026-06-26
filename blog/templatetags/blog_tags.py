from django import template
from blog.models import Comment, Post, Category
from django.utils import timezone
from taggit.models import Tag

register = template.Library()

@register.simple_tag(name='commentlength')
def function(pid):
    comments = Comment.objects.filter(post=pid, approved=True).count()

    return comments

@register.inclusion_tag('blog/blog-recent.html')
def recentposts():
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())[:6]

    return {'posts': posts}

@register.inclusion_tag('blog/blog-categories.html')
def categories():
    category = Category.objects.all()
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())
    cat_dict = {}

    for cat in category:
        cat_dict[cat] = posts.filter(category=cat).count()

    return {"categories": cat_dict}

@register.inclusion_tag('blog/blog-tags.html')
def alltags():
    tags = Tag.objects.all()

    return {'tags': tags}