from django.urls import path
from blog.views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_index, name='index'),
    path('<int:pid>', blog_single, name='single'),
    path('author/<str:auth_username>', blog_index, name='author'),
    path('category/<str:cat_name>', blog_index, name='category'),
    path('tag/<str:tag_name>', blog_index, name='tag'),
    path('like/<int:cid>', like_comment, name='like'),
    path('search/', blog_search, name='search')
]