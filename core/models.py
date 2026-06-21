from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('wip', 'In Progress'),
        ('learning', 'Learning Project'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    emoji = models.CharField(max_length=10, default='⚡')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='live')
    tags = models.CharField(max_length=500, help_text="Comma-separated: Django, HTMX, Tailwind")
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text="Lower = shown first")
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def get_badge_class(self):
        return {
            'live': 'badge-live',
            'wip': 'badge-wip',
            'learning': 'badge-fresh',
        }.get(self.status, 'badge-fresh')

    def get_badge_label(self):
        return {
            'live': 'Live',
            'wip': 'In Progress',
            'learning': 'Learning Project',
        }.get(self.status, self.status)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(max_length=400, help_text="Short summary shown on listing page")
    content = models.TextField(help_text="Full article content — HTML is supported")
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated tags")
    published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def read_time(self):
        words = len(self.content.split())
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject}"
