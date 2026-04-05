import streamlit as st
import requests
nei_list = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards',
            'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes', 'NoRidge',
            'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker']
api_url = 'http://127.0.0.1:8000/predict/'
st.title('Прогноз цены')
area = st.number_input('Площадь дома: ', value=0)
year = st.number_input('Год: ', value=0)
garage = st.number_input('Вместимость гаража: ', value=0)
bsmt = st.number_input('Площадь подвала: ', value=0)
bath = st.number_input('количество Ванны: ', value=0)
overall_qual = st.number_input('Качество: ', value=0)
neighborhood = st.selectbox('Район: ', nei_list)

data = {
    "GrLivArea": area,
    "YearBuilt": year,
    "GarageCars": garage,
    "TotalBsmtSF": bsmt,
    "FullBath": bath,
    "OverallQual": overall_qual,
    "Neighborhood": neighborhood
}

if st.button('Проверка'):
    try:
        answer = requests.post(api_url, json=data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.success(f'Результат: {result.get("Price")}')
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error(f'Не удалось подключиться к API')