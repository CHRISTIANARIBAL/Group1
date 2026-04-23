from django.contrib import admin
from .models import *

admin.site.register(Course)

admin.site.register(Progress)

class LessonContentInline(admin.TabularInline):
    model = LessonContent
    extra = 1  # 👈 this creates the "+" add row

class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonContentInline]

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Activity)
admin.site.register(Question)
admin.site.register(Choice)

