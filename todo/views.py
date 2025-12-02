from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Task  # You'll need to create a Task model
from django.utils import timezone


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        try:
            task = Task()
            task.title = request.POST.get('title', '')
            task.description = request.POST.get('description', '')
            
            created_at = request.POST.get('created_at')
            if created_at:
                task.created_at = created_at
            else:
                task.created_at = timezone.now()
            
            created_by = request.user
            if created_by:
                task.created_by = created_by
            
            # Save the task to the database
            task.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Task added successfully',
                'task_id': task.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })

def existing_tasks(request):
    """Return all tasks as JSON"""
    tasks = Task.objects.all().order_by('-created_at')
    
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at.isoformat()
        })
    
    return JsonResponse({
        'success': True,
        'tasks': task_list
    })



def delete_task(request, task_id):
    if request.method == "POST":
        try:
            task = get_object_or_404(Task, id=task_id)
            task.delete()
            return JsonResponse({
                'success': True,
                'message': 'Task deleted successfully'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })


def is_completed(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        if task.is_completed == True: 
            return JsonResponse({"error": "Task is already completed."}, status=400)
        if task.is_completed == False:
            task.is_completed = True
            task.save()
            return JsonResponse({
                'success': True,
                'message': 'Task marked as completed'
            })
        

def existing_tasks(request):
    # For your AJAX endpoint
    tasks = Task.objects.all().order_by('is_completed', '-created_at')
    tasks_data = []
    
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at.isoformat(),
            'created_by': task.created_by.username if task.created_by else 'Anonymous',
            'is_completed': task.is_completed
        })
    
    return JsonResponse({'success': True, 'tasks': tasks_data})