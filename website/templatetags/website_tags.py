from django import template
from blog.models import Post
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('website/website-recent.html')
def recentposts():
    posts = Post.objects.filter(published_status=True, published_date__lte=timezone.now())[:3]

    return {'posts': posts}