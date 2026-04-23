from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course, Lesson, Progress, LessonContent
from .forms import CourseForm, LessonForm

def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lessons')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            error = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            error = "Username already taken"
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')

    return render(request, 'register.html', {'error': error})

@login_required
def lessons(request):
    courses = Course.objects.all()
    return render(request, 'lessons.html', {'courses': courses})

@login_required
def course(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    # Get completed lessons of this user
    completed_lessons = Progress.objects.filter(
        user=request.user,
        completed=True
    ).values_list('lesson_id', flat=True)

    lesson_data = []
    unlocked = True  # first lesson is always unlocked

    for lesson in lessons:
        if lesson.id in completed_lessons:
            status = 'completed'
        elif unlocked:
            status = 'current'
            unlocked = False
        else:
            status = 'locked'

        lesson_data.append({
            'lesson': lesson,
            'status': status
        })

    return render(request, 'course.html', {
        'course': course,
        'lesson_data': lesson_data
    })

@login_required
def complete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    progress, created = Progress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    progress.completed = True
    progress.save()

    return redirect('course', course_id=lesson.course.id)

@login_required
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    contents = lesson.contents.all().order_by('order')

    # Next lesson
    next_lesson = Lesson.objects.filter(
        course=lesson.course,
        order__gt=lesson.order
    ).order_by('order').first()

    # Previous lesson 👇
    prev_lesson = Lesson.objects.filter(
        course=lesson.course,
        order__lt=lesson.order
    ).order_by('-order').first()

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'contents': contents,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson
    })

@login_required
def reset_progress(request, course_id):
    course = Course.objects.get(id=course_id)

    # Delete all progress for this course
    Progress.objects.filter(
        user=request.user,
        lesson__course=course
    ).delete()

    return redirect('course', course_id=course.id)

def is_admin(user):
    return user.is_staff  # only admin can access

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid credentials or not an admin."

    return render(request, 'admin/admin_login.html', {'error': error})

@user_passes_test(is_admin)
def admin_dashboard(request):
    course_count = Course.objects.count()
    lesson_count = Lesson.objects.count()
    content_count = LessonContent.objects.count()

    return render(request, 'admin/admin_dashboard.html', {
        'course_count': course_count,
        'lesson_count': lesson_count,
        'content_count': content_count,
    })

# LIST
@user_passes_test(is_admin)
def admin_courses(request):
    courses = Course.objects.all()
    return render(request, 'admin/courses.html', {'courses': courses})

# CREATE
@user_passes_test(is_admin)
def admin_add_course(request):
    form = CourseForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('admin_courses')

    return render(request, 'admin/course_form.html', {'form': form})

# UPDATE
@user_passes_test(is_admin)
def admin_edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    form = CourseForm(request.POST or None, instance=course)

    if form.is_valid():
        form.save()
        return redirect('admin_courses')

    return render(request, 'admin/course_form.html', {'form': form})

# DELETE
@user_passes_test(is_admin)
def admin_delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('admin_courses')

# LESSONS (placeholder for now)
@user_passes_test(is_admin)
def admin_lessons(request):
    return render(request, 'admin/lessons.html')

@user_passes_test(is_admin)
def admin_lessons(request):
    courses = Course.objects.all()

    return render(request, 'admin/lessons.html', {
        'courses': courses
    })

def admin_add_lesson(request, course_id):
    form = LessonForm(request.POST or None)

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
        return redirect('admin_course_lessons', course_id=course.id)

    return render(request, 'admin/lesson_form.html', {
        'form': form,
        'course_id': course.id,
        'course_obj': course   # 👈 ADD THIS
    })

# ✏️ UPDATE
def admin_edit_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    form = LessonForm(request.POST or None, instance=lesson)

    contents = LessonContent.objects.filter(lesson=lesson)

    # 👇 ADD THIS
    selected_course = lesson.course

    if form.is_valid():
        form.save()
        return redirect('admin_lessons')

    return render(request, 'admin/lesson_form.html', {
        'form': form,
        'lesson': lesson,
        'contents': contents,
        'course_id': selected_course.id,
        'course_obj': selected_course   # 👈 THIS IS THE FIX
    })

# ❌ DELETE
@user_passes_test(is_admin)
def admin_delete_lesson(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    lesson.delete()
    return redirect('admin_lessons')

# USERS LIST
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.all()
    return render(request, 'admin/users.html', {'users': users})

@user_passes_test(is_admin)
def admin_add_content(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        LessonContent.objects.create(
            lesson=lesson,
            title=request.POST.get('title'),
            text=request.POST.get('text'),
            image=request.FILES.get('image'),
            order=request.POST.get('order') or 0
        )
        return redirect('admin_edit_lesson', id=lesson.id)

    return render(request, 'admin/content_form.html', {'lesson': lesson})

@user_passes_test(is_admin)
def admin_course_lessons(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')

    return render(request, 'admin/course_lessons.html', {
        'course': course,
        'lessons': lessons
    })