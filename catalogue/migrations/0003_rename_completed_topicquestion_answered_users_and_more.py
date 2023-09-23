# Generated by Django 4.2.5 on 2023-09-23 03:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('catalogue', '0002_topicquestion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topicquestion',
            old_name='completed',
            new_name='answered_users',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='question_content_type',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='question_id',
        ),
        migrations.AlterField(
            model_name='topic',
            name='thread_reference',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='topicquestion',
            name='question_content_type',
            field=models.ForeignKey(blank=True, limit_choices_to={'app_label__istartswith': 'assessment', 'model__icontains': 'question'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_content_type', to='contenttypes.contenttype'),
        ),
    ]