import streamlit as st
import pandas as pd 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

st.subheader("심부전 환자 데이터")
st.dataframe(df.head(10))

avg = df['age'].mean()
st.metric(
    label="평균 나이",
    value=f"{avg:.1f}세"
)