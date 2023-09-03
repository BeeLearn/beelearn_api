# Generated by Django 4.1 on 2023-08-28 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('REWARD_ACHIEVE', 'Reward achieved'), ('LESSON_COMPLETE', 'Lesson completed'), ('STREAK_COMPLETE', 'Streak completed')], max_length=128)),
                ('xp', models.IntegerField()),
                ('bits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Streak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('streak_complete_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(choices=[('ACHIEVER', 'Achiever'), ('HAT_TRICK', 'Hat Trick'), ('COURSE_MASTER', 'Course Master'), ('COURSE_NINJA', 'Course Ninja'), ('VERIFY_ACCOUNT', 'Verify Account'), ('NEW_CAREER_AWAITS', 'New Career Awaits'), ('WHERE_THE_MAGIC_HAPPENS', 'Where The Magic Happens'), ('JUST_GETTING_STARTED', 'Just Getting Started'), ('FEARLESS', 'Fearless'), ('ENGAGED_IN', 'Engaged In'), ('WE_ARE_IN_THIS_TOGETHER', 'We Are In This Together')], max_length=128)),
                ('title', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=128)),
                ('icon', models.ImageField(upload_to='assets/rewards/icons')),
                ('color', models.CharField(max_length=11)),
                ('dark_color', models.CharField(max_length=11)),
                ('price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reward.price')),
                ('reward_unlocked_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
