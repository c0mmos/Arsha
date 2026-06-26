from django.contrib import admin
from website.models import Contact, NewsLetter

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'
    list_display = ['name', 'email', 'subject', 'created_date']
    list_filter = ('email', 'name')
    search_fields = ('name', 'subject', 'message')
    ordering = ['-created_date']

admin.site.register(NewsLetter)
admin.site.register(Contact, ContactAdmin)  