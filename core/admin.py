from django.contrib import admin
from .models import Course, Lesson, Progress, LessonContent

admin.site.register(Course)

admin.site.register(Progress)

class LessonContentInline(admin.TabularInline):
    model = LessonContent
    extra = 1  # 👈 this creates the "+" add row

class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonContentInline]

admin.site.register(Lesson, LessonAdmin)

