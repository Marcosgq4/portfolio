from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Task
from .forms import TaskForm

INCOMPLETE = 'Incomplete'
COMPLETE = 'Complete'

@login_required
def task_list(request):
    filters = {'user': request.user, 'status': 'Incomplete', 'is_deleted': False}

    most_important_tasks = Task.objects.filter(**filters, importance='most_important').order_by('due_date')
    very_important_tasks = Task.objects.filter(**filters, importance='very_important').order_by('due_date')
    important_tasks = Task.objects.filter(**filters, importance='important').order_by('due_date')
    not_important_tasks = Task.objects.filter(**filters, importance='not_important').order_by('due_date')
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')
        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
        except Task.DoesNotExist:
            pass
        
    task_categories = {
        'most_important_tasks': most_important_tasks,
        'very_important_tasks': very_important_tasks,
        'important_tasks': important_tasks,
        'not_important_tasks': not_important_tasks
    }
    
    return render(request, 'tasks/task_list.html', {'task_categories': task_categories})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_manager:task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'hide_add_task': True
    }
    return render(request, 'tasks/add_task.html', context)

@login_required
def completed_tasks(request):
    most_important_tasks = Task.objects.filter(is_deleted=False, user=request.user, status='Complete', importance='most_important').order_by('due_date')
    very_important_tasks = Task.objects.filter(is_deleted=False, user=request.user, status='Complete', importance='very_important').order_by('due_date')
    important_tasks = Task.objects.filter(is_deleted=False, user=request.user, status='Complete', importance='important').order_by('due_date')
    not_important_tasks = Task.objects.filter(is_deleted=False, user=request.user, status='Complete', importance='not_important').order_by('due_date')

    completed_task_categories = {
        'most_important_tasks': most_important_tasks,
        'very_important_tasks': very_important_tasks,
        'important_tasks': important_tasks,
        'not_important_tasks': not_important_tasks
    }

    return render(request, 'tasks/completed_tasks.html', {'completed_task_categories': completed_task_categories})

@login_required
def deleted_tasks(request):
    most_important_tasks = Task.objects.filter(user=request.user, is_deleted=True, importance='most_important').order_by('due_date')
    very_important_tasks = Task.objects.filter(user=request.user, is_deleted=True, importance='very_important').order_by('due_date')
    important_tasks = Task.objects.filter(user=request.user, is_deleted=True, importance='important').order_by('due_date')
    not_important_tasks = Task.objects.filter(user=request.user, is_deleted=True, importance='not_important').order_by('due_date')

    deleted_task_categories = {
        'most_important_tasks': most_important_tasks,
        'very_important_tasks': very_important_tasks,
        'important_tasks': important_tasks,
        'not_important_tasks': not_important_tasks
    }

    return render(request, 'tasks/deleted_tasks.html', {'deleted_task_categories': deleted_task_categories})

@require_POST
@login_required
def deleting_task(request):
    task_id = request.POST.get('task_id')
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        if task.is_deleted:  # Assuming 'Deleted' is a status for deleted tasks
            task.delete()
            return JsonResponse({'status': 'ok', 'message': 'Task permanently deleted.'})
        else:
            task.is_deleted = True
            task.save()
            return JsonResponse({'status': 'ok', 'message': 'Task marked as deleted.'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found.'})
    
    
@login_required
@require_POST
def update_task(request):
    task_id = request.POST.get('task_id')
        
    try:
        task = Task.objects.get(id=task_id)
        print(f"Task ID: {task.id}, Current Status: {task.status}")
        
        if task.user == request.user: 
            task.status = COMPLETE if task.status == INCOMPLETE else INCOMPLETE
            task.save()
            return JsonResponse({'status': 'ok', 'message': 'Task status successfully updated.'})
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized action.'}, status=403)
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found.'}, status=404)
    
@require_POST
@login_required
def restore_task(request):
    task_id = request.POST.get('task_id')
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        if task.is_deleted: 
            task.is_deleted = False
            task.save()
            return JsonResponse({'status': 'ok', 'message': 'Task restored.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Task is not deleted.'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found.'})
    
@require_POST
@login_required
def update_importance(request):
    task_id = request.POST.get('task_id')
    new_importance = request.POST.get('importance')
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        if new_importance in dict(Task.IMPORTANCE_CHOICES):
            task.importance = new_importance
            task.save()
            return JsonResponse({'status': 'ok', 'message': 'Importance updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid importance value.'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found.'})