from .db import Base
from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    admin = 'admin'
    seller = 'seller'
    buyer = 'buyer'


class PropertyType(str, PyEnum):
    apartment = 'apartment'
    house = 'house'
    plot = 'plot'
    commercial = 'commercial'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, create_constraint=False), default=UserRole.buyer)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    preferred_language: Mapped[str] = mapped_column(String(5), default='ru')

    properties: Mapped[List['Property']] = relationship(back_populates='seller',
                                                        cascade='all, delete-orphan')
    reviews_left: Mapped[List['Review']] = relationship(foreign_keys='Review.author_id',
                                                        back_populates='author',
                                                        cascade='all, delete-orphan')
    reviews_received: Mapped[List['Review']] = relationship(foreign_keys='Review.seller_id',
                                                            back_populates='seller')
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')

    def __str__(self):
        return self.username


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    token_user: Mapped['User'] = relationship(back_populates='user_token')
    token: Mapped[str] = mapped_column(String(512), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.token_user}, {self.token}'


class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))

    cities: Mapped[List['City']] = relationship(back_populates='region',
                                                cascade='all, delete-orphan')

    def __str__(self):
        return self.name


class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    name: Mapped[str] = mapped_column(String(100))

    region: Mapped['Region'] = relationship(back_populates='cities')
    districts: Mapped[List['District']] = relationship(back_populates='city',
                                                       cascade='all, delete-orphan')

    def __str__(self):
        return self.name


class District(Base):
    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    name: Mapped[str] = mapped_column(String(100))

    city: Mapped['City'] = relationship(back_populates='districts')

    def __str__(self):
        return self.name


class Property(Base):
    __tablename__ = 'property'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType, create_constraint=False))
    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey('region.id'), nullable=True)
    city_id: Mapped[Optional[int]] = mapped_column(ForeignKey('city.id'), nullable=True)
    district_id: Mapped[Optional[int]] = mapped_column(ForeignKey('district.id'), nullable=True)
    address: Mapped[str] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(Integer)
    area: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer, default=1)
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_floors: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    documents: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    seller: Mapped['User'] = relationship(back_populates='properties')
    region: Mapped[Optional['Region']] = relationship()
    city: Mapped[Optional['City']] = relationship()
    district: Mapped[Optional['District']] = relationship()
    images: Mapped[List['PropertyImage']] = relationship(back_populates='property',
                                                         cascade='all, delete-orphan')

    def __str__(self):
        return self.title


class PropertyImage(Base):
    __tablename__ = 'property_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    image: Mapped[str] = mapped_column(String)

    property: Mapped['Property'] = relationship(back_populates='images')

    def __str__(self):
        return f'{self.property_id}, {self.image}'


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    stars: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author: Mapped['User'] = relationship(foreign_keys=[author_id], back_populates='reviews_left')
    seller: Mapped['User'] = relationship(foreign_keys=[seller_id], back_populates='reviews_received')

    def __str__(self):
        return f'{self.author}, {self.rating}'