import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Project, BlogPost, ContactMessage


def home(request):
    projects = Project.objects.all()
    posts = BlogPost.objects.filter(published=True)[:3]
    return render(request, 'core/home.html', {
        'projects': projects,
        'posts': posts,
    })


@require_POST
def track_project_view(request, slug):
    """AJAX endpoint — increments view count when a project card is clicked."""
    project = get_object_or_404(Project, slug=slug)
    project.view_count += 1
    project.save(update_fields=['view_count'])
    return JsonResponse({'views': project.view_count})


def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    return render(request, 'core/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    return render(request, 'core/blog_detail.html', {'post': post})


@require_POST
def contact(request):
    name    = request.POST.get('name', '').strip()
    email   = request.POST.get('email', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()

    errors = []
    if not name:    errors.append('Name is required.')
    if not email:   errors.append('Email is required.')
    if not subject: errors.append('Subject is required.')
    if not message: errors.append('Message is required.')

    if errors:
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    # Save to DB
    ContactMessage.objects.create(
        name=name, email=email, subject=subject, message=message
    )

    # Send email notification
    try:
        send_mail(
            subject=f"[Portfolio] {subject} — from {name}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.EMAIL_HOST_USER or 'noreply@portfolio.com',
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass  # Message is already saved to DB — email is best-effort

    return JsonResponse({'ok': True})
