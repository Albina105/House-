from .views import UserAdmin, RefreshTokenAdmin, RegionAdmin, CityAdmin, DistrictAdmin, PropertyAdmin, PropertyImageAdmin, ReviewAdmin
from fastapi import FastAPI
from sqladmin import Admin
from mysite.database.db import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(DistrictAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(PropertyImageAdmin)
    admin.add_view(ReviewAdmin)