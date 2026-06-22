import streamlit as st 
import pandas as pd 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

age_max = st.slider(
    "최대나이", 40, 95, 70
) # 40, 95, 70 = 최소, 최대, 시작값

filtered = df[df['age'] <= age_max]
st.write(f"{len(filtered)}명이 조건에 맞아요")

st.dataframe(filtered)