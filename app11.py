import streamlit as st 

def home():
    st.title("홈")

def data():
    st.title("데이터")
    
pg = st.naviagtion([
    st.page(home, title = '홈',
            icon = '❤️', default = True),
    st.page(data, title = '데이터',
            icon = '🎶')               
])

pg.run()