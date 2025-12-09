from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from .tasks import send_invoice_email

def place_order(request):
    # pretend this saves an order
    order_id = 1234  # this would come from your model

    # run the task in the background
    send_invoice_email.delay(order_id)

    return JsonResponse({"message": "Order placed successfully!"})
