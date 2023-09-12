# Generated by Django 4.1 on 2023-09-10 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='content',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='small_image',
            new_name='icon',
        ),
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='notification',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='topic',
            field=models.TextField(choices=[('IN_APP', 'In-app'), ('GENERAL', 'General'), ('COMMENTS', 'Comments')], default=''),
            preserve_default=False,
        ),
    ]
