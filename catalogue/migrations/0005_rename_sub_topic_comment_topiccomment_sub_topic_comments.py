# Generated by Django 4.1 on 2023-09-04 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_topiccomment_sub_topic_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topiccomment',
            old_name='sub_topic_comment',
            new_name='sub_topic_comments',
        ),
    ]
