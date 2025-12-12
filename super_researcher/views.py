from .tasks import run_super_researcher
from django.http import JsonResponse
from mcp_server import ModelQueryToolset
from models import SuperResearcher

def save_researcher(request):
    if request.method == "POST":
        run_super_researcher.delay()
        
