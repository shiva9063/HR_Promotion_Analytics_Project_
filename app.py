import streamlit as st
import pandas as pd
import joblib
import pickle
st.title('HR Analystics')

# features:
# 'department', 'education', 'gender', 'recruitment_channel',
# 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service',
# 'KPIs_met >80%', 'awards_won?', 'avg_training_score'

with st.form('entry form'):
    col1,col2=st.columns(2)
    with col1:

        department_options=['Sales & Marketing','Operations',
                'Technology','Procurement',
                'Analytics','Finance','HR',
                'Legal','R&D']
        department=st.selectbox('select the department',department_options)

        education_options=["Bachelor's","Master's & above","Below Secondary",]
        education=st.selectbox('select the education',education_options)

        gender=st.radio('select gender',['Male','Female'])

        recruitment_channel=st.selectbox('select recruitment',['sourcing','referred','other'])

        no_of_trainings=st.slider('select the no of trainings',min_value=1,max_value=10)

        age=st.number_input('enter age of employee',min_value=18,max_value=100,format='%d')
    with col2:

        previous_year_rating=st.slider('enter the previous year rating',min_value=1,max_value=5)

        length_of_service=st.number_input('enter the no of years service',min_value=1,format='%d')

        KPIs_met=st.radio('KPIs_met >80%',[1,0]) 

        awards_won=st.radio('Award won',[1,0]) 

        avg_training_score=st.number_input('avg_training_score',min_value=1,format='%d')
    submited=st.form_submit_button('submit entries')

# Dataframe for the given inputs
df=pd.DataFrame({
    'department':[department],
    'education':[education],
    'gender':[gender],
    'recruitment_channel':[recruitment_channel],
    'no_of_trainings':[no_of_trainings],
    'age':[age],
    'previous_year_rating':[previous_year_rating],
    'length_of_service':[length_of_service],
    'KPIs_met >80%':[KPIs_met],
    'awards_won?':[awards_won],
    'avg_training_score':[avg_training_score]
})

object_columns=["department", "education", "gender",'recruitment_channel']
# loading the model
model=joblib.load('models/model.h5')

# loading label encoding 
# --- Load encoders and model ---
with open("models/label_encoders.pkl", "rb") as f:
    encoders = pickle.load(f)
for col,val in encoders.items():
    if col in df.columns:
        df[col]=val.transform(df[col])
# loading scaler
# Load scaler later

scaler = joblib.load("models/minmax_scaler.pkl")
df_scaled= scaler.transform(df)
df_for_pred = pd.DataFrame(df_scaled, columns=df.columns)


def prediction(model,data):
    predict=model.predict(data)
    if predict==0:
        st.error('Not Promoted')
    else:
        st.success('Promoted')
prediction(model,df_for_pred)