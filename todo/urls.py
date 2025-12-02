from django.urls import path
from .views import *

urlpatterns = [
    # Existing URLs
    path("add_task/", add_task, name="add_task"),
    path("existing_tasks/", existing_tasks, name="existing_tasks"),
    path("toggle-task/<int:task_id>/", toggle_task, name="toggle_task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete_task"),
    path("get-task/<int:task_id>/", get_task, name="get_task"),
    path("update-task/<int:task_id>/", update_task, name="update_task"),
]