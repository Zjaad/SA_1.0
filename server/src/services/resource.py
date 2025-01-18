from sqlalchemy.orm import Session
from src.models.resource import Resource
from src.schemas.resource import ResourceCreate, ResourceUpdate

class ResourceService:
    @staticmethod
    async def create_resource(db: Session, resource: ResourceCreate):
        db_resource = Resource(**resource.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource

    @staticmethod
    async def get_resource(db: Session, resource_id: int):
        return db.query(Resource).filter(Resource.id == resource_id).first()

    @staticmethod
    async def get_subject_resources(db: Session, subject_id: int):
        return db.query(Resource).filter(Resource.subject_id == subject_id).all()

    @staticmethod
    async def update_resource(db: Session, resource_id: int, resource: ResourceUpdate):
        db_resource = await ResourceService.get_resource(db, resource_id)
        if db_resource:
            for key, value in resource.dict(exclude_unset=True).items():
                setattr(db_resource, key, value)
            db.commit()
            db.refresh(db_resource)
        return db_resource
