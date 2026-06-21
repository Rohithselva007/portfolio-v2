from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('emoji', models.CharField(default='⚡', max_length=10)),
                ('status', models.CharField(choices=[('live', 'Live'), ('wip', 'In Progress'), ('learning', 'Learning Project')], default='live', max_length=20)),
                ('tags', models.CharField(help_text='Comma-separated: Django, HTMX, Tailwind', max_length=500)),
                ('live_url', models.URLField(blank=True)),
                ('github_url', models.URLField(blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower = shown first')),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['order', '-created_at']},
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('excerpt', models.TextField(help_text='Short summary shown on listing page', max_length=400)),
                ('content', models.TextField(help_text='Full article content — HTML is supported')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags', max_length=300)),
                ('published', models.BooleanField(default=False)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField()),
                ('subject', models.CharField(max_length=300)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
