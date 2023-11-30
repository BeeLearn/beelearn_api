from django.contrib import admin

from nested_admin import NestedStackedInline, NestedModelAdmin

from .models import Course, Lesson, Category, Module, Topic, TopicQuestion


class TopicInline(NestedStackedInline):
    model = Topic
    extra = 1


class LessonInline(NestedStackedInline):
    model = Lesson
    inlines = (TopicInline,)
    extra = 1


class ModuleInline(NestedStackedInline):
    model = Module
    inlines = (LessonInline,)
    extra = 1


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    inlines = (ModuleInline,)
    extra = 1

    list_display = (
        "id",
        "creator",
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


class TopicQuestionInline(admin.StackedInline):
    model = TopicQuestion
    extra = 1

    autocomplete_lookup_fields = {
        "generic": [
            [
                "question_content_type",
                "question_id",
            ]
        ],
    }


@admin.register(TopicQuestion)
class TopicQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "number_of_answered_users",
        "question_created_at",
        "question_updated_at",
    )

    def question(self, instance: TopicQuestion):
        return instance.question.title

    def question_created_at(self, instance: TopicQuestion):
        return instance.question.created_at

    def question_updated_at(self, instance: TopicQuestion):
        return instance.question.updated_at

    def number_of_answered_users(self, instance: TopicQuestion):
        return instance.answered_users.count()

    autocomplete_lookup_fields = {
        "generic": [
            [
                "question_content_type",
                "question_id",
            ],
        ],
    }


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_visible",
        "thread_reference",
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

    inlines = (TopicQuestionInline,)

    # form = TopicAdminForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
