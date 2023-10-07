# Generated by Django 4.2.5 on 2023-10-01 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='icon',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='topic',
            field=models.TextField(choices=[('ADS', 'ads'), ('COMMENTS', 'comments')]),
        ),
    ]