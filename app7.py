import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots()
ax.hist(df['age'], bins = 20,
           color = '#5BAFB8')
ax.set_xlabel("나이")
ax.set_ylabel("환자 수")

st.pyplot(fig)
