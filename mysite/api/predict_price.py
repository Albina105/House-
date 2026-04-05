import joblib
from fastapi import FastAPI, APIRouter
from mysite.database.schema import HouseSchema
nei_list = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards',
            'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge',
            'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker']

model = joblib.load('mysite/ml_models/model.pkl')
scaler = joblib.load('mysite/ml_models/scaler.pkl')
predict_router = APIRouter(prefix='/predict', tags=['House Price'])
@predict_router.post('/')
async def predict_price(house: HouseSchema):
    house_dict = house.dict()
    name_nei = house_dict.pop('Neighborhood')
    name_nei1_0 = [
        1 if name_nei == i else 0 for i in nei_list
    ]
    house_data = list(house_dict.values()) + name_nei1_0
    scaled_data = scaler.transform([house_data])
    pred = model.predict(scaled_data)[0]
    return {'Price': round(pred)}