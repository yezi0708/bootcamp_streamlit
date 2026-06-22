import streamlit as st
import pandas as pd 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

st.subheader(" 환자 데이터")
st.dataframe(df.head())

st.metric(
    label = "전체 환자 수",
    value = f"{len(df)}명",
    delta = "299건 수집"
)