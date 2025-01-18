from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.resource import Resource, ResourceCreate, ResourceUpdate
from src.services.resource import ResourceService
from src.services.auth import get_current_user

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("", response_model=Resource)
async def create_resource(
    resource: ResourceCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await ResourceService.create_resource(db, resource)

@router.get("/subject/{subject_id}", response_model=List[Resource])
async def get_subject_resources(
    subject_id: int,
    db: Session = Depends(get_db)
):
    return await ResourceService.get_subject_resources(db, subject_id)

@router.get("/{resource_id}", response_model=Resource)
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = await ResourceService.get_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/{resource_id}", response_model=Resource)
async def update_resource(
    resource_id: int,
    resource: ResourceUpdate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_resource = await ResourceService.update_resource(db, resource_id, resource)
    if not updated_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_resource
