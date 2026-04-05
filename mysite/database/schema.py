from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import UserRole, PropertyType


class UserInputSchema(BaseModel):
    username: str
    email: str
    password: str
    phone_number: Optional[str] = None
    role: UserRole = UserRole.buyer
    preferred_language: str = 'ru'

class UserOutSchema(BaseModel):
    id: int
    username: str
    email: str
    phone_number: Optional[str] = None
    role: UserRole
    preferred_language: str


class RegionInputSchema(BaseModel):
    name: str

class RegionOutSchema(BaseModel):
    id: int
    name: str


class CityInputSchema(BaseModel):
    region_id: int
    name: str

class CityOutSchema(BaseModel):
    id: int
    region_id: int
    name: str


class DistrictInputSchema(BaseModel):
    city_id: int
    name: str

class DistrictOutSchema(BaseModel):
    id: int
    city_id: int
    name: str


class PropertyInputSchema(BaseModel):
    seller_id: int
    title: str
    description: str
    property_type: PropertyType
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    district_id: Optional[int] = None
    address: str
    price: int
    area: int
    rooms: int = 1
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    documents: Optional[str] = None

class PropertyOutSchema(BaseModel):
    id: int
    seller_id: int
    title: str
    description: str
    property_type: PropertyType
    region_id: Optional[int] = None
    city_id: Optional[int] = None
    district_id: Optional[int] = None
    address: str
    price: int
    area: int
    rooms: int
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    documents: Optional[str] = None
    created_at: datetime


class PropertyImageInputSchema(BaseModel):
    property_id: int
    image: str

class PropertyImageOutSchema(BaseModel):
    id: int
    property_id: int
    image: str


class ReviewInputSchema(BaseModel):
    author_id: int
    seller_id: int
    stars: int
    rating: int
    comment: str

class ReviewOutSchema(BaseModel):
    id: int
    author_id: int
    seller_id: int
    stars: int
    rating: int
    comment: str
    created_at: datetime


class UserLoginSchema(BaseModel):
    username: str
    password: str

class HouseSchema(BaseModel):
    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: str


