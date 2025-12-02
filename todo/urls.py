from django.urls import path
from .views import *

urlpatterns = [
    # Existing URLs
    path("add-task/", add_task, name="add_task"),
    path("existing-tasks/", existing_tasks, name="existing_task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete_task"),
    ]