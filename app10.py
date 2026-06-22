import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

# 왼쪽 사이드바에 필터를 준다
st.sidebar.header(" 필터")
age = st.sidebar.slider("최대 나이", 
                        40, 95, 70)

df = df[df['age'] <= age]

tab1, tab2 = st.tabs(["표", "차트"])
                      
with tab1: 
    st.dataframe(df)
    
with tab2:
    fig, ax = plt.subplots()
    ax.hist(df['age'], bins = 20)
    st.pyplot(fig)
