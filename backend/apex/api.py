from ninja import ModelSchema, Router
from .models import apex_research
from .scrap import main
from .models import apex_research


class Apex_schema(ModelSchema):
    class Meta:
        model = apex_research
        model_fields = [
            'id',
            'company',
            'website',
            'phone_number',
            'email',
            'full_name',
            'promoted',
            'is_active_lead',
            'lead_class',
            'notes',
            'address',
        ]

apex_router = Router()

@apex_router.get("/home")
def apex_home(request, pk: int, payload : Apex_schema ):
    tenders = main()
    return {"tenders": tenders}


@apex_router.get("/contacts")
def get_apex_research_contacts(request, pk: int, payload : Apex_schema ):
    """Retrieves all non-promoted Apex Research contacts."""
    apex_contacts = apex_research.objects.filter(promoted=False)
    return {"apex_contacts": list(apex_contacts.values())}


@apex_router.post("/contacts")
def add_apex_research_contact(request,  pk: int, payload : Apex_schema ):
    """Creates a new Apex Research contact."""
    apex_contact = apex_research.objects.create(
        company=payload.company,
        website=payload.website,
        phone_number=payload.phone_number,
        email=payload.email,
        full_name=payload.full_name,
        is_active_lead=payload.is_active_lead,
        lead_class=payload.lead_class,
        notes=payload.notes,
        address=payload.address,
        promoted=False
    )
    return {"success": True, "message": "Apex Research contact added successfully", "id": apex_contact.id}


@apex_router.post("/contacts/{contact_id}/promote")
def promote_apex_research_contact(request, contact_id: int, payload : Apex_schema):
    """Marks an Apex Research contact as promoted."""
    try:
        contact = apex_research.objects.get(pk=contact_id)
        contact.promoted = True
        contact.save()
        return {"success": True, "message": "Contact promoted successfully"}
    except apex_research.DoesNotExist:
        return {"success": False, "error": "Contact not found"}