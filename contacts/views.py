from sms import send_sms
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404   
from .models import Contact, sent_emails, sent_sms
from .forms import ContactForm
from django.template.loader import get_template
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from apex.models import apex_research
from super_researcher.models import SuperResearcher

def contact_list_view(request):
    """Main view for displaying and filtering the contact list.
    
    Handles filtering by lead classification, searching by name/email/phone,
    and sorting contacts by specified fields. Renders the index template
    with contacts and filter/sort parameters.
    
    Args:
        request: Django request object containing GET parameters for filtering,
                 searching, and sorting.
    
    Returns:
        HttpResponse: Rendered index.html template with contacts and filter options.
    """
    if request.user.is_authenticated:
        lead_class = request.GET.get('lead_class')
        search_query = request.GET.get('search')
        sort_by = request.GET.get('sort_by', 'Full_name')
        
        contacts = Contact.objects.all()
        
        if lead_class:
            contacts = contacts.filter(lead_class=lead_class)
        
        if search_query:
            contacts = contacts.filter(
                Q(Full_name__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        contacts = contacts.order_by(sort_by)
        
        return render(request, 'index.html', {
            'contacts': contacts,
            'leads': contacts,
            'current_filter': lead_class,
            'search_query': search_query,
            'sort_by': sort_by,
            'lead_classifications': Contact.LEAD_CLASSIFICATIONS
        })
    else: 
        return redirect('/accounts/login/')


def contact_detail_view(request, contact_id):
    """Displays detailed contact information and handles inline editing.
    
    Shows a single contact's details and allows for inline editing of all fields.
    Supports both AJAX and standard form submissions for updates.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact to display/edit.
    
    Returns:
        HttpResponse: Rendered more_contact_info.html template or JSON response
                     for AJAX requests.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    
    if request.method == 'POST':
        contact.Full_name = request.POST.get('Full_name', contact.Full_name)
        contact.email = request.POST.get('email', contact.email)
        contact.lead_class = request.POST.get('lead_class', contact.lead_class)
        contact.phone_number = request.POST.get('phone_number', contact.phone_number)
        contact.address = request.POST.get('address', contact.address)
        contact.company = request.POST.get('company', contact.company)
        contact.notes = request.POST.get('notes', contact.notes)
        
        try:
            contact.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Contact updated successfully'})
            else:
                return redirect('more_contact_info', contact_id=contact_id)
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'more_contact_info.html', {'contact': contact,
                                                      "LEAD_CLASSIFICATIONS": Contact.LEAD_CLASSIFICATIONS,
                                                      'send_emails': sent_emails.objects.filter(contact=contact).order_by('-sent_at')})


def create_contact_view(request):
    """Handles manual creation of a new contact.
    
    Processes the ContactForm and sets the creation timestamp before saving.
    Redirects to the contact list on success.
    
    Args:
        request: Django request object containing form data.
    
    Returns:
        HttpResponse: Redirect to index on success or rendered adding_contact.html
                     with form on GET/error.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.created_at = timezone.now()
            contact.save()
            return redirect('/index')
    else:
        form = ContactForm()
    return render(request, 'adding_contact.html', {'form': form})


def edit_contact_view(request, contact_id):
    """Handles editing an existing contact using Django forms.
    
    Displays a pre-populated ContactForm for the specified contact.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact to edit.
    
    Returns:
        HttpResponse: Redirect to index on success or rendered update_contact.html
                     with form on GET/error.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('/index')
    else:
        form = ContactForm(instance=contact)
    
    return render(request, 'update_contact.html', {
        'form': form, 
        'contact': contact
    })


@csrf_protect
def delete_contact_view(request, contact_id):
    """Handles deletion of a contact.
    
    Deletes the specified contact via POST request and returns JSON response.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact to delete.
    
    Returns:
        JsonResponse: Success/failure status and message.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    if request.method == 'POST':
        try:
            contact = get_object_or_404(Contact, id=contact_id)
            contact_name = contact.Full_name
            if contact_name == '':
                contact_name = 'Unnamed Contact'
            contact.delete()
            return JsonResponse({'success': True, 'message': f'Contact {contact_name} deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def compose_email_view(request, contact_id):
    """Renders the email composition template for a specific contact.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact.
    
    Returns:
        HttpResponse: Rendered email.html template with contact context.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, "email.html", {'contact': contact})


def send_email_view(request, contact_id):
    """Sends an email to a contact and logs the communication.
    
    Sends email via Django's send_mail, creates a database record of the sent
    email, and updates lead status from 'New' to 'Contacted' if applicable.
    
    Args:
        request: Django request object with subject and message POST data.
        contact_id: Primary key of the Contact to email.
    
    Returns:
        JsonResponse: Success/failure status, message, and redirect URL.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    if request.method == "POST":
        try:
            contact = get_object_or_404(Contact, pk=contact_id)
            recip_email = contact.email
            
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            from_email = recip_email
            
            if not all([subject, message]):
                return JsonResponse({
                    'success': False, 
                    'error': 'Subject and message are required'
                })
            
            sent = send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[contact.email],
                fail_silently=False,
            )

            emails = sent_emails.objects.create(
                contact=contact,
                subject=subject,
                message=message,
                sent_at=timezone.now(),
                from_email=from_email,
                sent_by=request.user if request.user.is_authenticated else None
            )
            if sent == True: 
                print("Email sent successfully")
                print("Shifting from new to Contacted")
                Updated_contact = contact.lead_class
                if Updated_contact == "New":
                    contact.lead_class = "Contacted"
                    contact.save()
            print("Saved the sent email to the database")

            return JsonResponse({
                'success': True, 
                'message': 'Text sent successfully',
                'redirect': '/index'
            })
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Email sending error: {str(e)}")
            
            return JsonResponse({
                'success': False, 
                'error': f'Failed to send email: {str(e)}'
            })
    else: 
        return JsonResponse({
            'success': False, 
            'error': 'Invalid request method'
        })


def compose_sms_view(request, contact_id):
    """Renders the SMS composition template for a specific contact.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact.
    
    Returns:
        HttpResponse: Rendered message.html template with contact context.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, "message.html", {'contact': contact})



def send_sms_message_view(request, contact_id):
    """Sends an SMS to a contact and logs the communication.
    
    Uses SMS service to send message, creates a database record, and updates
    lead status from 'New' to 'Contacted' if applicable.
    
    Args:
        request: Django request object with body POST data.
        contact_id: Primary key of the Contact to message.
    
    Returns:
        JsonResponse: Success/failure status, message, and redirect URL on POST.
        HttpResponse: Rendered message.html template on GET.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    company_number = "0424854899"
    contact = get_object_or_404(Contact, pk=contact_id)
    
    if request.method == 'POST':
        try:
            recip_number = contact.phone_number
            body = request.POST.get('body')
            sent_at = timezone.now()
            
            if not all([body, recip_number]):
                return JsonResponse({
                    'success': False, 
                    'error': 'Need body and number'
                })
                
            sms = send_sms(
                body=body,
                originator=company_number,
                recipients=[recip_number]
            )

            sms_record = sent_sms.objects.create(
                contact=contact,
                body=body,
                sent_at=sent_at
            )
            
            if sms:
                print("SMS sent successfully")
                print("Shifting from new to Contacted")
                Updated_contact = contact.lead_class
                if Updated_contact == "New":
                    contact.lead_class = "Contacted"
                    contact.save()
            
            print("Saved the sent SMS to the database")
            return JsonResponse({
                'success': True, 
                'message': 'Text sent successfully',
                'redirect': '/index'
            })

        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"SMS sending error: {str(e)}")
            
            return JsonResponse({
                'success': False, 
                'error': f'Failed to send SMS: {str(e)}'
            })
    
    else:
        return render(request, "message.html", {'contact': contact})
    

def sent_emails_history_view(request):
    """Displays all sent emails ordered by most recent first.
    
    Renders index.html with a list of all sent email communications
    for viewing email history across all contacts.
    
    Args:
        request: Django request object.
    
    Returns:
        HttpResponse: Rendered index.html template with emails context.
    """
    emails = sent_emails.objects.all().order_by('-sent_at')
    return render(request, 'index.html', {'emails': emails})


def contact_detail_form_view(request, contact_id):
    """Alternative detailed contact view using Django forms.
    
    Displays contact details with a pre-populated ContactForm and handles
    both AJAX and standard form submissions.
    
    Args:
        request: Django request object.
        contact_id: Primary key of the Contact to display/edit.
    
    Returns:
        HttpResponse: Rendered contact_detail.html template or JSON response
                     for AJAX requests.
    
    Raises:
        Http404: If contact with given ID does not exist.
    """
    contact = get_object_or_404(Contact, pk=contact_id)
    sent_emails = sent_emails.objects.filter(contact=contact).order_by('-sent_at')
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Contact updated successfully'})
            return redirect('contact_detail', contact_id=contact.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = ContactForm(instance=contact)
    
    context = {
        'contact': contact,
        'sent_emails': sent_emails,
        'form': form,
    }
    return render(request, 'contact_detail.html', context)


def communication_logs_view(request):
    if request.method == "POST":
        email_logs = sent_emails.objects.all().order_by('-sent_at')
        sms_logs = sent_sms.objects.all().order_by('-sent_at')
        email_list = [{"id": e.id, "contact": e.contact.Full_name, "subject": e.subject, "message": e.message, "sent_at": e.sent_at} for e in email_logs]
        sms_list = [{"id": s.id, "contact": s.contact.Full_name, "body": s.body, "sent_at": s.sent_at} for s in sms_logs]
        return JsonResponse({"emails": email_list, "sms": sms_list})



def promote_apex(request, contact_id):
    if request.method == "POST":
        contact = get_object_or_404(apex_research, pk=contact_id)
        if contact == None:
            return JsonResponse({'success': False, 'error': 'Contact not found'})
        if contact:
            contact.promoted = True
            contact.save()
            return JsonResponse({'success': True, 'message': 'Contact promoted successfully'})

def promote_super(request, contact_id):
    if request.method == "POST":
        contact = get_object_or_404(SuperResearcher, pk=contact_id)
        if contact == None:
            return JsonResponse({'success': False, 'error': 'Contact not found'})
        if contact:
            contact.promoted = True
            contact.save()
            return JsonResponse({'success': True, 'message': 'Contact promoted successfully'})
        
def show_promoted_contacts(request):
    if request.method == "POST":
        promoted_apex_contacts = apex_research.objects.filter(promoted=True)
        promoted_super_contacts = SuperResearcher.objects.filter(promoted=True)
        return JsonResponse({
            'apex_contacts': promoted_apex_contacts,
            'super_contacts': promoted_super_contacts
        })
    

# Del for prod


def render_apex(request):
    if request.method == "POST" or request.method == "GET":
        apex_contacts = apex_research.objects.filter(promoted=False)
        return JsonResponse({'apex_contacts': list(apex_contacts.values())})

def add_apex(request):
    if request.method == "POST":
        company = request.POST.get("company")
        website = request.POST.get("website")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")

        apex_contact = apex_research.objects.create(
            company=company,
            website=website,
            phone_number=phone_number,
            email=email,
            full_name=full_name,
            promoted=False
        )
        return render(request, "add_apex.html", {'success': True, 'message': 'Apex Research contact added successfully'})
    else:
        return render(request, "add_apex.html")
    

def render_super(request):
    if request.method == "POST" or request.method == "GET":
        super_contacts = SuperResearcher.objects.all()
        return JsonResponse({'super_contacts': list(super_contacts.values())})

def add_super(request):
    if request.method == "POST":
        company = request.POST.get("company")
        website = request.POST.get("website")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        full_name = request.POST.get("full_name")

        super_contact = SuperResearcher.objects.create(
            company=company,
            website=website,
            phone_number=phone_number,
            email=email,
            full_name=full_name,
            promoted=False
        )
        return render(request, "add_super.html", {'success': True, 'message': 'Super Researcher contact added successfully'})
    else:
        return render(request, "add_super.html")
    

def staged_leads(request):
    if request.method == "POST" or request.method == "GET":
        apex_leads = apex_research.objects.filter(promoted=True)
        super_leads = SuperResearcher.objects.filter(promoted=True)
        return JsonResponse({
            'apex_leads': list(apex_leads.values()),
            'super_leads': list(super_leads.values())
        })
    

def promote_to_active(request):
    if request.method == "POST" or request.method == "GET":
        apex_leads = apex_research.objects.filter(promoted=True)
        super_leads = SuperResearcher.objects.filter(promoted=True)
        if apex_leads:
            for contact in apex_leads:
                contact.is_active_lead = True
                contact.save()
        if super_leads:
            for contact in super_leads:
                contact.is_active_lead = True
                contact.save()
        return JsonResponse({
            'apex_leads': list(apex_leads.values()),
            'super_leads': list(super_leads.values())
        })
    
def active_leads_view(request):
    if request.method == "POST" or request.method == "GET":
        promoted_apex_contacts = apex_research.objects.filter(promoted=True)
        promoted_super_contacts = SuperResearcher.objects.filter(promoted=True)
        if promoted_apex_contacts or promoted_super_contacts:
            promoted_apex_contacts.update(promoted=False)
            promoted_super_contacts.update(promoted=False)
             
        active_apex_leads = apex_research.objects.filter(is_active_lead=True)
        active_super_leads = SuperResearcher.objects.filter(is_active_lead=True)
        return JsonResponse({
            'active_apex_leads': list(active_apex_leads.values()),
            'active_super_leads': list(active_super_leads.values())
        })