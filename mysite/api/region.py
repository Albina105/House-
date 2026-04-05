from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import Region
from mysite.database.schema import RegionInputSchema, RegionOutSchema



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

region_router = APIRouter(prefix='/regions', tags=['Region'])

@region_router.post('/', response_model=RegionOutSchema)
async def create_region(region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = Region(**region.dict())
    db.add(region_db)
    db.commit()
    db.refresh(region_db)
    return region_db

@region_router.get('/', response_model=List[RegionOutSchema])
async def list_regions(db: Session = Depends(get_db)):
    return db.query(Region).all()

@region_router.get('/{region_id}', response_model=RegionOutSchema)
async def get_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='Region not found', status_code=404)
    return region_db

@region_router.put('/{region_id}', response_model=dict)
async def update_region(region_id: int, region: RegionInputSchema, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='Region not found', status_code=404)
    for region_key, region_value in region.dict().items():
        setattr(region_db, region_key, region_value)
    db.commit()
    db.refresh(region_db)
    return {'message': 'Region был успешно изменен!'}

@region_router.delete('/{region_id}', response_model=dict)
async def delete_region(region_id: int, db: Session = Depends(get_db)):
    region_db = db.query(Region).filter(Region.id == region_id).first()
    if not region_db:
        raise HTTPException(detail='Region not found', status_code=404)
    db.delete(region_db)
    db.commit()
    return {'message': 'Region был успешно удален!'}


