from django.urls import path
from .views import *

urlpatterns = [
    # Existing URLs
    path("add_task/", add_task, name="add_task"),
    path("existing_tasks/", existing_tasks, name="existing_tasks"),
    ]