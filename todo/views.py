from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task  # You'll need to create a Task model

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        try:
            # Get form data
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            priority = request.POST.get('priority', 'medium')
            category = request.POST.get('category', 'general')
            due_date = request.POST.get('due_date')
            completed = request.POST.get('completed') == 'on'
            
            # Create task
            task = Task.objects.create(
                title=title,
                description=description,
                priority=priority,
                category=category,
                due_date=due_date if due_date else None,
                completed=completed
            )
            
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
            'priority': task.priority,
            'category': task.category,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        })
    
    return JsonResponse({
        'success': True,
        'tasks': task_list
    })

@csrf_exempt
def toggle_task(request, task_id):
    """Toggle task completion status"""
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            
            return JsonResponse({
                'success': True,
                'completed': task.completed
            })
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Task not found'
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

@csrf_exempt
def delete_task(request, task_id):
    """Delete a task"""
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Task deleted successfully'
            })
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Task not found'
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

def get_task(request, task_id):
    """Get task details for editing"""
    try:
        task = Task.objects.get(id=task_id)
        
        return JsonResponse({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'priority': task.priority,
                'category': task.category,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'completed': task.completed
            }
        })
    except Task.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Task not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
def update_task(request, task_id):
    """Update an existing task"""
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            
            # Update fields
            task.title = request.POST.get('title', task.title)
            task.description = request.POST.get('description', task.description)
            task.priority = request.POST.get('priority', task.priority)
            task.category = request.POST.get('category', task.category)
            due_date = request.POST.get('due_date')
            task.due_date = due_date if due_date else None
            task.completed = request.POST.get('completed') == 'on'
            
            task.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Task updated successfully'
            })
        except Task.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Task not found'
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