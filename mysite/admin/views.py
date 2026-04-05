from mysite.database.models import User, RefreshToken, Region, City, District, Property, PropertyImage, Review
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role]

class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_at]

class RegionAdmin(ModelView, model=Region):
    column_list = [Region.id, Region.name]

class CityAdmin(ModelView, model=City):
    column_list = [City.id, City.name, City.region_id]

class DistrictAdmin(ModelView, model=District):
    column_list = [District.id, District.name, District.city_id]

class PropertyAdmin(ModelView, model=Property):
    column_list = [Property.id, Property.title, Property.seller_id, Property.property_type, Property.price]

class PropertyImageAdmin(ModelView, model=PropertyImage):
    column_list = [PropertyImage.id, PropertyImage.property_id, PropertyImage.image]

class ReviewAdmin(ModelView, model=Review):
    column_list = [Review.id, Review.author_id, Review.seller_id, Review.rating]