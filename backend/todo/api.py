from ninja import NinjaAPI, ModelSchema
from ninja.security import django_auth
from .models import Todo
from django.shortcuts import get_object_or_404
from typing import List

# Schemas
class TodoSchema(ModelSchema):
    class Meta:
        model = Todo
        fields = [
            'id',
            'title',
            'description',
            'date',
            'completed',
            'priority',
            'created_by',
        ]



todo_api = NinjaAPI(auth=django_auth)

@todo_api.get("/index", response=List[TodoSchema])
def todo_list(request):
    """Get all todos ordered by date (newest first)"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    todos = Todo.objects.order_by("-date")
    return 200, todos

@todo_api.get("/stats", response=dict)
def todo_stats(request):
    """Get todo statistics (total, pending, completed)"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    total_count = Todo.objects.count()
    pending_count = Todo.objects.filter(completed=False).count()
    completed_count = Todo.objects.filter(completed=True).count()

    return 200, {
        'total': total_count,
        'pending': pending_count,
        'completed': completed_count
    }

@todo_api.post("/add", response=TodoSchema)
def create_todo(request, payload: TodoSchema):
    """Create a new todo"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    todo = Todo.objects.create(
        title=payload.title,
        description=payload.description or '',
        priority=payload.priority or 'medium',
        created_by=request.user
    )

    return 201, todo

@todo_api.get("/moreinfo/{todo_id}", response=TodoSchema)
def todo_detail(request, todo_id: int):
    """Get a single todo by ID"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    todo = get_object_or_404(Todo, pk=todo_id)
    return 200, todo

@todo_api.post("/update/{todo_id}", response=TodoSchema)
def update_todo(request, todo_id: int, payload: TodoSchema):
    """Update an existing todo"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    try:
        todo = Todo.objects.get(pk=todo_id)
        todo.title = payload.title
        todo.description = payload.description
        todo.priority = payload.priority
        todo.completed = payload.completed
        todo.save()
        return 200, todo
    except Todo.DoesNotExist:
        return 404, {'error': 'Todo not found'}

@todo_api.delete("/delete/{todo_id}")
def delete_todo(request, todo_id: int):
    """Delete a todo"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    try:
        todo = get_object_or_404(Todo, pk=todo_id)
        todo_title = todo.title if todo.title else 'Unnamed Todo'
        todo.delete()
        return 200, {'success': True, 'message': f'Todo {todo_title} deleted successfully'}
    except Exception as e:
        return 500, {'success': False, 'error': str(e)}

@todo_api.post("/toggle/{todo_id}", response=TodoSchema)
def toggle_todo(request, todo_id: int):
    """Toggle todo completion status"""
    if not request.user.is_authenticated:
        return 403, {'error': 'Authentication required'}

    try:
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.completed = not todo.completed
        todo.save()
        return 200, todo
    except Exception as e:
        return 500, {'success': False, 'error': str(e)}