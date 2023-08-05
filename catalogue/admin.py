from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Course, Lesson, Category, Module, Topic


class TopicInline(NestedStackedInline):
    model = Topic
    extra = 1


class LessonInline(NestedStackedInline):
    model = Lesson
    extra = 1
    inlines = [TopicInline]


class ModuleInline(NestedStackedInline):
    model = Module
    extra = 1
    inlines = [LessonInline]


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(NestedModelAdmin):
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(NestedModelAdmin):
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
