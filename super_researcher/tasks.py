from celery import shared_task

@shared_task
def send_invoice_email():
    print(f"Sending invoice email for order order_id")