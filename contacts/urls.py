from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='contact_list'),
    path('add/', adding_contact, name='add_contact'),
]

