from .models import Course, Module, Lesson, Topic, TopicQuestion


def down():
    Course.course_enrolled_users.through.objects.all().delete()
    Course.course_complete_users.through.objects.all().delete()

    Module.entitled_users.through.objects.all().delete()
    Module.module_complete_users.through.objects.all().delete()

    Lesson.lesson_complete_users.through.objects.all().delete()
    Lesson.entitled_users.through.objects.all().delete()

    Topic.entitled_users.through.objects.all().delete()
    Topic.likes.through.objects.all().delete()
    Topic.topic_complete_users.through.objects.all().delete()

    TopicQuestion.answered_users.through.objects.all().delete()
