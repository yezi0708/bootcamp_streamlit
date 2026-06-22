import streamlit as st 
import pandas as pd 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

choice = st.selectbox(
    "성별", ["남성", "여성"])

code = 1 if choice == "남성" else 0 
result = df[df['sex'] == code]

only_death = st.checkbox("사망 환자만 보기")
if only_death:
    result = result[result['DEATH_EVENT'] == 1]

st.write(f"{len(result)}명")
st.dataframe(result)