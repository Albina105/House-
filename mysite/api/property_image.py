from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import PropertyImage
from mysite.database.schema import PropertyImageInputSchema, PropertyImageOutSchema



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

property_image_router = APIRouter(prefix='/property-images', tags=['PropertyImage'])

@property_image_router.post('/', response_model=PropertyImageOutSchema)
async def create_property_image(image: PropertyImageInputSchema, db: Session = Depends(get_db)):
    image_db = PropertyImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db

@property_image_router.get('/', response_model=List[PropertyImageOutSchema])
async def list_property_images(db: Session = Depends(get_db)):
    return db.query(PropertyImage).all()

@property_image_router.get('/{image_id}', response_model=PropertyImageOutSchema)
async def get_property_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if not image_db:
        raise HTTPException(detail='PropertyImage not found', status_code=404)
    return image_db

@property_image_router.put('/{image_id}', response_model=dict)
async def update_property_image(image_id: int, image: PropertyImageInputSchema, db: Session = Depends(get_db)):
    image_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if not image_db:
        raise HTTPException(detail='PropertyImage not found', status_code=404)
    for image_key, image_value in image.dict().items():
        setattr(image_db, image_key, image_value)
    db.commit()
    db.refresh(image_db)
    return {'message': 'PropertyImage был успешно изменен!'}

@property_image_router.delete('/{image_id}', response_model=dict)
async def delete_property_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if not image_db:
        raise HTTPException(detail='PropertyImage not found', status_code=404)
    db.delete(image_db)
    db.commit()
    return {'message': 'PropertyImage был успешно удален!'}