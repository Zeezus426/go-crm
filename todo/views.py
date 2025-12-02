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


def task_list(request):
    # Fetch incomplete tasks for the current user
    incomplete_tasks = Task.objects.filter(
        created_by=request.user,
        is_completed=False
    ).order_by('-created_at') # Newest incomplete tasks first

    # Fetch completed tasks for the current user
    completed_tasks = Task.objects.filter(
        created_by=request.user,
        is_completed=True
    ).order_by('-created_at') # Newest completed tasks first

    context = {
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks': completed_tasks,
    }
    return JsonResponse({
        'success': True,
        'tasks': task_list
    })

def complete_task(request, task_id):
    # Get the specific task, or return a 404 error if not found
    task = get_object_or_404(Task, id=task_id)

    # Update the task's status
    task.is_completed = True
    # You might also want to update a 'completed_at' timestamp if you add one
    task.completed_at = timezone.now()
    task.save()

    # Redirect back to the task list page
    return JsonResponse({'success': True, 'message': 'Task marked as completed'})


def filter_tasks(request):
    """
    Filters tasks based on the 'is_completed' query parameter.
    - GET /api/tasks/?is_completed=true -> Returns only completed tasks.
    - GET /api/tasks/?is_completed=false -> Returns only incomplete tasks.
    - GET /api/tasks/ -> Returns all tasks.
    """
    # Start with a base queryset of all tasks
    tasks = Task.objects.all()

    # Get the filter parameter from the URL
    is_completed_param = request.GET.get('is_completed')

    # If the parameter exists, apply the filter
    if is_completed_param is not None:
        # Convert string 'true'/'false' to a boolean
        is_completed = is_completed_param.lower() == 'true'
        tasks = tasks.filter(is_completed=is_completed)

    # Order the final queryset by creation date (newest first)
    tasks = tasks.order_by('-created_at')

    # Serialize the task data for the JSON response
    tasks_data = [
        {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at.isoformat(),
            'created_by': task.created_by.username if task.created_by else 'Anonymous',
            'is_completed': task.is_completed,
        }
        for task in tasks
    ]

    return JsonResponse({'success': True, 'tasks': tasks_data})
