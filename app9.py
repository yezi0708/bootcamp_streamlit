import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv(r"D:\bootcamp\bootcamp_train\heart_failure.csv")

# 왼쪽 사이드바에 필터를 준다
st.sidebar.header(" 필터")
age = st.sidebar.slider("최대 나이", 
                        40, 95, 70)

df = df[df['age'] <= age]

# 본문을 둘로 나눈다
c1, c2 = st.columns(2)
c1.metric("환자 수", len(df))
c2.metric("평균 나이", f"{df.age.mean():.0f}")

# extra: 평균나이 별 생존확률
survival_rate = df.groupby("age")["DEATH_EVENT"].mean()

fig, ax = plt.subplots()
ax.plot(survival_rate.index, survival_rate.values)

ax.set_xlabel("나이")
ax.set_ylabel("사망률")

st.pyplot(fig)