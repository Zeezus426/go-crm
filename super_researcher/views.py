from .tasks import run_super_researcher
from django.http import JsonResponse

def return_super_results(request):
    run_super_researcher.apply_async(countdown=3600)
    
    return JsonResponse({"status": "Super Researcher task has been scheduled to run in 1 hour."})