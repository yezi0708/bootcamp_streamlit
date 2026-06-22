import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
plt.rcParams['axes.unicode_minus'] = False

counts = df['DEATH_EVENT'].value_counts()
st.subheader("Survived vs Death")

# 방법 a: 내장 차트
st.bar_chart(counts)

# 방법 b: matplotlib
fig, ax = plt.subplots()
ax.bar(["Survived", "Death"], counts,
       color = ['#edafb8', '#0077b6'])
       
st.pyplot(fig)