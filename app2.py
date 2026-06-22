import streamlit as st

st.title(" 건강 데이터 탐험기")
st.write("이 앱은 의료 데이터를 쉽게 살펴보는 도구입니다.")

name = st.text_input("이름을 입력하세요")

if name:
    st.write(f"반갑습니다, {name}님! 함께 시작해요")
    
else:
    st.info("위에 이름을 입력하면 인사를 드릴게요.")