# Generated by Django 4.2.5 on 2023-09-14 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='intent_to',
        ),
    ]
