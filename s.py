import pandas as pd
import streamlit as st
import joblib
import datetime

model = joblib.load(r"C:\Users\PC\Desktop\mansvi\Random_forest_model (2)\Random_forest_model (2).pkl")


st.title("Energy consumption Predictor")
model_columns = [
    'num_occupants',
    'house_size_sqft',
    'monthly_income',
    'outside_temp_celsius',
    'year',
    'month',
    'day',
    'season',
    'heating_type_Electric',
    'heating_type_Gas',
    'heating_type_None',
    'cooling_type_AC',
    'cooling_type_Fan',
    'cooling_type_None',
    'manual_override_Y',
    'manual_override_N',
    'is_weekend',
    'temp_above_avg',
    'income_per_person',
    'square_feet_per_person',
    'high_income_flag',
    'low_temp_flag',
    'season_spring',
    'season_summer',
    'season_fall',
    'season_winter',
    'day_of_week_0',
    'day_of_week_6',
    'energy_star_home'
    
]

num_occupants=st.number_input("Number of Occupants",min_value=3,value=5)
house_size_sqft=st.number_input("house size sqrt",min_value=1000,value=2000)
monthly_income=st.number_input("monthly_incom",min_value=1000,value=2000)
outside_temp_celsius=st.number_input("outside temperature in c",min_value=22,value=26)
year=st.number_input("year ",min_value=2001,max_value=2060,value=2025)
month=st.number_input("month",min_value=5,max_value=12,value=8)
day=st.number_input("day",min_value=1,max_value=31,value=1)

obj=datetime.date(year,month,day)
day_of_week=obj.weekday()



if month in [12,1,2]:
    season_label="winter"
elif month in [3,4,5]:
    season_label="summer"
elif month in [6,7,8]:
    season_label="Rain"
else:
    season_label="spring"
    
    
heating_type=st.selectbox("Heating types",["Electric","Gas","None"])
cooling_type=st.selectbox("cooling type",["Ac","Fan","None"])
manual_override=st.radio("manual override",["Y","N"])
energy_star_home=st.checkbox("certified home",value=False)

#derived parametrs
is_weekend=int(day_of_week>=5)
temp_above_avg=int(outside_temp_celsius>28)
income_per_person=monthly_income/num_occupants
square_feet_per_person=house_size_sqft/num_occupants
high_income_flag=int(monthly_income>40000)
low_temp_flag=int(outside_temp_celsius<28)

data={
    'num_occupants':num_occupants,
    'house_size_sqft':house_size_sqft,
    'monthly_income':monthly_income,
    'outside_temp_celsius':outside_temp_celsius,
    'year':year,
    'month':month,
    'day':day,
    'season':0,
    'heating_type_Electric':int(heating_type=="Electric"),
    'heating_type_Gas':int(heating_type=="Gas"),
    'heating_type_None':int(heating_type=="None"),
    'cooling_type_AC':int(cooling_type=="Ac"),
    'cooling_type_Fan':int(cooling_type=="Fan"),
    'cooling_type_None':int(cooling_type=="None"),
    'manual_override_Y':int(manual_override=="Y"),
    'manual_override_N':int(manual_override=="N"),
    'is_weekend':is_weekend,
    'temp_above_avg':temp_above_avg,
    'income_per_person':income_per_person,
    'square_feet_per_person':square_feet_per_person,
    'high_income_flag':high_income_flag,
    'low_temp_flag':low_temp_flag,
    'season_spring':int(season_label=="spring"),
    'season_summer':int(season_label=="summer"),
    'season_fall':int(season_label=="fall"),
    'season_winter':int(season_label=="winter"),
    'day_of_week_0':int(day_of_week==0),
    'day_of_week_6':int(day_of_week==6),
    'energy_star_home':int(energy_star_home)
    
}
input_df = pd.DataFrame([data])           
input_df = input_df[model_columns]        

if st.button("🔮 Predict"):
    prediction = model.predict(input_df)[0]
    st.success(f"⚡ Prediction: {prediction:.2f} kWh")
