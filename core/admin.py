from django.contrib import admin
from .models import Project, BlogPost, ContactMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'featured', 'order', 'view_count', 'created_at']
    list_editable = ['status', 'featured', 'order']
    list_filter = ['status', 'featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'view_count', 'read_time', 'created_at']
    list_editable = ['published']
    list_filter = ['published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'read', 'created_at']
    list_editable = ['read']
    list_filter = ['read']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']

    def has_add_permission(self, request):
        return False  # Messages only come in via contact form
