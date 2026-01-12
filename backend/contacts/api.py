from ninja import NinjaAPI, ModelSchema
from .models import Contact, sent_emails, sent_sms
from django.db.models import Q

class ContactSchema(ModelSchema):
    class Meta:
        model = Contact
        model_fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company',
            'position',
            'notes',
        ]

class SentEmailSchema(ModelSchema):
    class Meta:
        model = sent_emails
        model_fields = [
            'id',
            'contact',
            'subject',
            'body',
            'sent_at',
        ]


class SentSmsSchema(ModelSchema):
    class Meta:
        model = sent_sms
        model_fields = [
            'id',
            'contact',
            'body',
            'sent_at',
        ]
api = NinjaAPI()

@api.get("/contacts", response=ContactSchema)
def contact_list(request):
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
