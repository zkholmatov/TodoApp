from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Task
from django.db.models import Q
from django.utils import timezone
from .forms import TaskForm
from django.utils.timezone import now


# Create your views here.
def task(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if q == '':
        print("Empty")
    else:
        print(f"Searching for: {q}")

    tasks = Task.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )

    no_tasks = not tasks.exists()

    if request.method == 'POST':
        new_task = Task.objects.create(
            name = request.POST.get('task-name'),
            due_date = request.POST.get('due-date')
        )

    for task in tasks:
        if task.due_date == timezone.now().date():
            task.is_due_today = True
        elif task.due_date < timezone.now().date():
            task.overdue = True
        if task.completed_date:
            task.completed_today = True if task.completed_date == timezone.now().date() else False

    return render(request, 'base/tasks.html', {'tasks': tasks, 'no_tasks': no_tasks, 'q': q})


def taskForm(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data['name']
            task_description = form.cleaned_data['description']
            task_due_date = form.cleaned_data['due_date']

            task = Task.objects.create(
                name = task_name,
                description = task_description,
                due_date = task_due_date
            )

            task.save()
            return redirect('task')

    context = {'form': form}
    return render(request, 'base/task_form.html', context)


def completeTask(request, pk):
    task = Task.objects.get(id=pk)
    
    # if request.user != task.user:
    #     return HttpResponse('You are not allowed here')

    if request.method == 'GET':
        task.complete = True
        task.priority = False
        task.completed_date = timezone.now()
        task.save()
        return redirect('task')

    return redirect('task')


def incompleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'GET':
        task.complete = False
        task.completed_date = None
        task.save()
        return redirect('task')

    return redirect('task')


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'GET':
        task.delete()
        return redirect('task')

    return redirect('task')


def toggleDescription(request, pk):
    task = Task.objects.get(id=pk)
    tasks = Task.objects.all()

    if request.method == 'GET':
        for item in tasks:
            if item.expand == True:
                item.expand = False
                item.save()
                
        task.expand = not task.expand
        task.save()

        return redirect('task')

    return redirect('task')


def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    # setting form manually
    # form = TaskForm(instance=task)

    # if request.method == 'POST':
    #     task.name = request.POST.get('name')
    #     task.description = request.POST.get('description')
    #     task.due_date = request.POST.get('due_date')
    #     task.priority = request.POST.get('priority') == 'on'
    #     task.save()
    #     return redirect('task')


    # setting form autimatically
    form = TaskForm(request.POST or None, instance=task)

    if request.method == 'POST':
        form.save()
        return redirect('task')


    context = {'form': form, 'task': task}
    return render(request, 'base/task_form.html', context)