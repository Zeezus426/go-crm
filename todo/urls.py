from django.urls import path
from .views import *

urlpatterns = [
    # Existing URLs
    path("add-task/", add_task, name="add_task"),
    path('tasks/', task_list, name='task_list'),
    
    # The URL to complete a specific task. It captures the task's ID.
    path('tasks/<int:task_id>/complete/', complete_task, name='complete_task'),
    path("delete-task/<int:task_id>/", delete_task, name="delete_task"),
    # path('todo/is-completed/<int:task_id>/', is_completed, name='is_completed'),

    ]