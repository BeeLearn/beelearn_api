# Generated by Django 4.2.3 on 2023-07-23 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reward', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='streak',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streak',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='streak',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='streak',
            constraint=models.UniqueConstraint(fields=('user', 'date'), name='User can only create one streak instance for a date'),
        ),
    ]
