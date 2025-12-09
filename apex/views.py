from django.shortcuts import render
from .scrap import main
# Create your views here.


def apex_home(request):
    tenders = main()
    context = {
        'tenders': tenders
    }
    return render(request, 'apex/apex_home.html', context)