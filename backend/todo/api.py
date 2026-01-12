from ninja import Router
from ninja.orm import create_schema
from .models import Todo
from typing import List

router = Router()

# Schemas
TodoSchema = create_schema(Todo, depth=1)
TodoCreateSchema = create_schema(Todo, exclude=['id', 'date'], depth=1)

# Todo Endpoints
@router.get("", response=List[TodoSchema])
def list_todos(request):
    return Todo.objects.all()

@router.get("/{todo_id}", response=TodoSchema)
def get_todo(request, todo_id: int):
    return Todo.objects.get(id=todo_id)

@router.post("", response=TodoSchema)
def create_todo(request, data: TodoCreateSchema):
    todo = Todo.objects.create(**data.dict())
    return todo

@router.put("/{todo_id}", response=TodoSchema)
def update_todo(request, todo_id: int, data: TodoCreateSchema):
    todo = Todo.objects.get(id=todo_id)
    for attr, value in data.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo

@router.delete("/{todo_id}")
def delete_todo(request, todo_id: int):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return {"success": True}