from django.urls import path
from . import views
# Arbitrary urls will be sunsetted in favour of the django ninja api points
# No longer used
app_name = 'super_researcher'

urlpatterns = [
    path("render-super/", views.get_super_researcher_contacts, name="render_super"),
    path('generate-leads/', views.generate_ai_leads, name='generate_ai_leads'),
    path("add_super/", views.add_super_researcher_contact, name="add_super"),
    path("super_test/", views.promote_super_researcher_contact, name="super_test_"),


]