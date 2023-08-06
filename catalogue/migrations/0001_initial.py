# Generated by Django 4.1 on 2023-08-06 02:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to=pathlib.PurePosixPath('assets/courses/backgrounds'))),
                ('description', models.TextField(blank=True, help_text='Course detailed description (Optional)', max_length=255, null=True)),
                ('course_complete_users', models.ManyToManyField(blank=True, related_name='course_complete_users', to=settings.AUTH_USER_MODEL)),
                ('course_enrolled_users', models.ManyToManyField(blank=True, related_name='course_enrolled_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=60)),
                ('entitled_users', models.ManyToManyField(blank=True, related_name='lesson_entitled_users', to=settings.AUTH_USER_MODEL)),
                ('lesson_complete_users', models.ManyToManyField(blank=True, related_name='lesson_complete_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('content', models.JSONField()),
                ('type', models.TextField(choices=[('TEXT', 'TEXT'), ('DRAG_DROP', 'Drag Drop'), ('TEXT_OPTION', 'TEXT_OPTION'), ('SINGLE_CHOICE', 'Multiple Choice'), ('MULTIPLE_CHOICE', 'Multiple Choice')])),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=128)),
                ('content', models.TextField()),
                ('entitled_users', models.ManyToManyField(blank=True, related_name='topic_entitled_users', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.lesson')),
                ('likes', models.ManyToManyField(blank=True, related_name='topic_likes', to=settings.AUTH_USER_MODEL)),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogue.question')),
                ('topic_complete_users', models.ManyToManyField(blank=True, related_name='topic_complete_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TopicComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=60)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.course')),
                ('entitled_users', models.ManyToManyField(blank=True, related_name='module_entitled_users', to=settings.AUTH_USER_MODEL)),
                ('module_complete_users', models.ManyToManyField(blank=True, related_name='complete_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.module'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.TextField(max_length=60)),
                ('courses', models.ManyToManyField(blank=True, to='catalogue.course')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
    ]
