from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm

def task_list(request):
    task_list = Task.objects.all().order_by('-due_date')  # Получаем список задач, отсортированный по сроку выполнения
    paginator = Paginator(task_list, 5)  # Создаем объект Paginator, 5 задач на страницу

    page_number = request.GET.get('page')  # Получаем номер страницы из запроса
    page_obj = paginator.get_page(page_number)  # Получаем объект страницы

    return render(request, 'tasks/task_list.html', {'page_obj': page_obj})


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_edit.html', {'form': form})

def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form})

def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')
