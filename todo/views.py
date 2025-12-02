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

def existing_tasks():
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



def del_tasks(request, contact_id):
    if request.method == "POST":
        try:
            task = get_object_or_404(Task, id=contact_id)
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
