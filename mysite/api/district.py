from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from mysite.database.db import SessionLocal
from mysite.database.models import District
from mysite.database.schema import DistrictInputSchema, DistrictOutSchema



async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

district_router = APIRouter(prefix='/districts', tags=['District'])

@district_router.post('/', response_model=DistrictOutSchema)
async def create_district(district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = District(**district.dict())
    db.add(district_db)
    db.commit()
    db.refresh(district_db)
    return district_db

@district_router.get('/', response_model=List[DistrictOutSchema])
async def list_districts(db: Session = Depends(get_db)):
    return db.query(District).all()

@district_router.get('/{district_id}', response_model=DistrictOutSchema)
async def get_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail='District not found', status_code=404)
    return district_db

@district_router.put('/{district_id}', response_model=dict)
async def update_district(district_id: int, district: DistrictInputSchema, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail='District not found', status_code=404)
    for district_key, district_value in district.dict().items():
        setattr(district_db, district_key, district_value)
    db.commit()
    db.refresh(district_db)
    return {'message': 'District был успешно изменен!'}

@district_router.delete('/{district_id}', response_model=dict)
async def delete_district(district_id: int, db: Session = Depends(get_db)):
    district_db = db.query(District).filter(District.id == district_id).first()
    if not district_db:
        raise HTTPException(detail='District not found', status_code=404)
    db.delete(district_db)
    db.commit()
    return {'message': 'District был успешно удален!'}