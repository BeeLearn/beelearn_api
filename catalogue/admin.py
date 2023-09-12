from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import Course, Lesson, Category, Module, Topic, TopicComment


class TopicInline(NestedStackedInline):
    model = Topic


class LessonInline(NestedStackedInline):
    model = Lesson
    inlines = (TopicInline,)


class ModuleInline(NestedStackedInline):
    model = Module
    inlines = (LessonInline,)


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    inlines = (ModuleInline,)

    list_display = (
        "id",
        "name",
        "is_visible",
        "number_of_enrolled_users",
        "number_of_completed_users",
        "created_at",
        "updated_at",
    )

    search_fields = ("name",)

    list_filter = (
        "created_at",
        "updated_at",
        "is_visible",
    )

    def number_of_completed_users(self, course: Course):
        return course.course_complete_users.count()

    def number_of_enrolled_users(self, course: Course):
        return course.course_enrolled_users.count()


@admin.register(Module)
class ModuleAdmin(NestedModelAdmin):
    inlines = (LessonInline,)

    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = ("name",)

    list_filter = (
        "created_at",
        "updated_at",
        "is_visible",
    )


@admin.register(Lesson)
class LessonAdmin(NestedModelAdmin):
    inlines = (TopicInline,)

    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "module__name",
        "module__course__name",
    )

    list_filter = (
        "created_at",
        "updated_at",
        "is_visible",
    )


class TopicAdminForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question_content_type"].queryset = ContentType.objects.filter(
            model__icontains="question",
        )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_visible",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "lesson__name",
        "lesson__module__name",
        "lesson__module__course__name",
    )

    list_filter = (
        "is_visible",
        "created_at",
        "updated_at",
    )

    form = TopicAdminForm


@admin.register(TopicComment)
class TopicCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "topic",
        "is_parent",
        "content",
        "created_at",
        "updated_at",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
