from ninja import Router
from ninja.orm import create_schema
from .models import SuperResearcher
from typing import List

router = Router()

# Schemas
SuperResearcherSchema = create_schema(SuperResearcher, depth=1)
SuperResearcherCreateSchema = create_schema(SuperResearcher, exclude=['id'], depth=1)

# Super Researcher Endpoints
@router.get("", response=List[SuperResearcherSchema])
def list_super_researcher(request):
    return SuperResearcher.objects.all()

@router.get("/{researcher_id}", response=SuperResearcherSchema)
def get_super_researcher(request, researcher_id: int):
    return SuperResearcher.objects.get(id=researcher_id)

@router.post("", response=SuperResearcherSchema)
def create_super_researcher(request, data: SuperResearcherCreateSchema):
    researcher = SuperResearcher.objects.create(**data.dict())
    return researcher

@router.put("/{researcher_id}", response=SuperResearcherSchema)
def update_super_researcher(request, researcher_id: int, data: SuperResearcherCreateSchema):
    researcher = SuperResearcher.objects.get(id=researcher_id)
    for attr, value in data.dict().items():
        setattr(researcher, attr, value)
    researcher.save()
    return researcher

@router.delete("/{researcher_id}")
def delete_super_researcher(request, researcher_id: int):
    researcher = SuperResearcher.objects.get(id=researcher_id)
    researcher.delete()
    return {"success": True}