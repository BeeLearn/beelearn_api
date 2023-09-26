# Generated by Django 4.2.5 on 2023-09-26 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reward', '0002_alter_reward_type'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='price',
            constraint=models.UniqueConstraint(fields=('type', 'xp', 'bits'), name='Price must be unique', violation_error_message='Price already exist'),
        ),
    ]
