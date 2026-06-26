from django.contrib import admin
from blog.models import Category, Post, Comment

class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    list_display = ('title','author','counted_views','published_status','published_date','created_date')
    list_filter = ('published_status', 'author')
    search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    list_display = ('name','email','subject','approved','created_date')
    list_filter = ('name', 'post', 'approved')
    search_fields = ('name', 'subject')

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)