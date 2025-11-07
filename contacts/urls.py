from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('add/', adding_contact, name='adding_contact'),  # MUST have name='adding_contact'

]

