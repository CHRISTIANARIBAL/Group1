from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    content = models.TextField(blank=True)  # 👈 ADD THIS

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    
class LessonContent(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200, blank=True) 
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.lesson.title} - Content {self.order}"

