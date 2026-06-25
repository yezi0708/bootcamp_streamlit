# 26.06.25 - 심부전 환자 분석 대시보드 (Advanced Version)
# 위젯 2개 이상 ✅, 레이아웃 1개 이상 ✅, session_state ✅, 꾸미기 ✅

import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ========== 데이터 로드 ==========
@st.cache_data
def load_data():
    df1 = pd.read_csv("heart.csv")
    df2 = pd.read_csv("heart_failure.csv")
    return df1, df2

df1, df2 = load_data()

# ========== 페이지 설정 ==========
st.set_page_config(
    page_title="💓 심부전 환자 분석 대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS 스타일링 ==========
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .title-section {
        border-bottom: 3px solid #FF6B6B;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Session State 초기화 ==========
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 50
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ========== 예측 모델 학습 ==========
@st.cache_resource
def train_model():
    # 데이터 전처리
    X = df2.drop('DEATH_EVENT', axis=1)
    y = df2['DEATH_EVENT']
    
    # 모델 학습
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, X.columns

model, feature_names = train_model()

# ========== 사이드바 메뉴 ==========
with st.sidebar:
    st.markdown("## 📱 메뉴")
    st.divider()
    
    page = st.radio(
        "페이지 선택",
        ["❤️ 나의 상태를 파악해요!", "💚 건강 정보를 공유해요!"],
        label_visibility="hidden"
    )

selected_page = "나의 상태를 파악해요!" if "❤️" in page else "건강 정보를 공유해요!"

# ========== 페이지1: 개인 진단 ==========
if selected_page == "나의 상태를 파악해요!":
    
    # 헤더 이미지
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(r"D:\bootcamp\bootcamp_train\img.png", width=120)
    with col_title:
        st.markdown("# 💓 심부전 위험도 분석")
        st.markdown("*당신의 심장 건강을 함께 지켜봅시다*")
    
    st.divider()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🏥 나의 상태 점검", "📊 Reports", "👥 Community"])
    
    # ==================== TAB 1: 나의 상태 점검 ====================
    with tab1:
        st.markdown("### 📋 개인 정보 및 증상 입력")
        
        # 개인 정보 입력
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.user_name = st.text_input(
                "👤 이름",
                value=st.session_state.user_name,
                placeholder="이름을 입력하세요"
            )
        
        with col2:
            st.session_state.user_age = st.slider(
                "🎂 나이",
                min_value=20, max_value=100,
                value=st.session_state.user_age
            )
        
        with col3:
            gender = st.selectbox("👨👩 성별", ["남성", "여성"])
        
        st.markdown("---")
        
        # 증상 입력
        st.markdown("### 🩺 건강 정보 입력")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chest_pain = st.checkbox("💔 흉통이 있으신가요?")
            high_bp = st.checkbox("⬆️ 고혈압이 있으신가요?")
            diabetes = st.checkbox("🩸 당뇨병이 있으신가요?")
            smoking = st.checkbox("🚬 흡연 경험이 있으신가요?")
        
        with col2:
            anaemia = st.checkbox("🩸 빈혈이 있으신가요?")
            
            serum_sodium = st.slider(
                "🧂 혈청 나트륨 (mEq/L)",
                min_value=100, max_value=150,
                value=130
            )
            
            ejection_fraction = st.slider(
                "💓 박출률 (%)",
                min_value=10, max_value=80,
                value=40
            )
        
        st.markdown("---")
        
        # 분석 버튼
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            analyze_btn = st.button("📊 내 상태 분석", use_container_width=True, type="primary")
        
        with col2:
            reset_btn = st.button("🔄 초기화", use_container_width=True)
        
        if reset_btn:
            st.session_state.user_name = ""
            st.session_state.user_age = 50
            st.session_state.analysis_done = False
            st.rerun()
        
        # 분석 실행
        if analyze_btn:
            if not st.session_state.user_name:
                st.error("⚠️ 이름을 입력해주세요!")
            else:
                st.session_state.analysis_done = True
                
                # 입력 데이터 저장
                st.session_state.user_data = {
                    'name': st.session_state.user_name,
                    'age': st.session_state.user_age,
                    'sex': 1 if gender == '남성' else 0,
                    'anaemia': anaemia,
                    'high_blood_pressure': high_bp,
                    'diabetes': diabetes,
                    'smoking': smoking,
                    'serum_sodium': serum_sodium,
                    'ejection_fraction': ejection_fraction
                }
                
                st.success(f"✅ {st.session_state.user_name}님의 데이터가 저장되었습니다!")
                st.balloons()
        
        # 분석 결과 표시
        if st.session_state.analysis_done:
            st.markdown("---")
            st.markdown("### 📈 분석 결과")
            
            # 위험도 예측
            user_features = np.array([[
                st.session_state.user_data['age'],
                1 if st.session_state.user_data['anaemia'] else 0,
                100,  # creatinine_phosphokinase (기본값)
                1 if st.session_state.user_data['diabetes'] else 0,
                st.session_state.user_data['ejection_fraction'],
                1 if st.session_state.user_data['high_blood_pressure'] else 0,
                150000,  # platelets (기본값)
                1.2,  # serum_creatinine (기본값)
                st.session_state.user_data['serum_sodium'],
                st.session_state.user_data['sex'],
                1 if st.session_state.user_data['smoking'] else 0,
                100  # time (기본값)
            ]]).reshape(1, -1)
            
            risk_probability = model.predict_proba(user_features)[0][1]
            risk_level = "🔴 높음" if risk_probability > 0.7 else "🟡 중간" if risk_probability > 0.4 else "🟢 낮음"
            
            # 메트릭 표시
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="사망 위험도",
                    value=risk_level,
                    delta=f"{risk_probability*100:.1f}%"
                )
            
            with col2:
                st.metric(
                    label="건강 점수",
                    value=f"{(1-risk_probability)*100:.0f}/100",
                    delta="높을수록 좋음"
                )
            
            with col3:
                st.metric(
                    label="권장 조치",
                    value="의료 상담" if risk_probability > 0.5 else "정기 검진"
                )
            
            # 위험 요소 분석 (파이 차트)
            risk_factors = {
                '나이': min(st.session_state.user_data['age'] / 100, 1),
                '박출률': 1 - (st.session_state.user_data['ejection_fraction'] / 80),
                '혈청나트륨': max(0, (145 - st.session_state.user_data['serum_sodium']) / 10),
                '당뇨병': 0.5 if st.session_state.user_data['diabetes'] else 0,
                '흡연': 0.5 if st.session_state.user_data['smoking'] else 0,
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=risk_factors.keys(),
                values=[v*100 for v in risk_factors.values()],
                hole=0.3,
                marker=dict(colors=['#FF6B6B', '#FFA500', '#FFD93D', '#6BCB77', '#4D96FF'])
            )])
            
            fig_pie.update_layout(
                title_text="위험 요소 분석",
                height=400,
                showlegend=True,
                font=dict(size=12)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # ==================== TAB 2: Reports ====================
    with tab2:
        st.markdown("### 📊 나의 리포트")
        
        if st.session_state.user_name:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👤 이름", st.session_state.user_name)
            with col2:
                st.metric("🎂 나이", f"{st.session_state.user_data.get('age', 0)}세")
            with col3:
                st.metric("💓 박출률", f"{st.session_state.user_data.get('ejection_fraction', 0)}%")
            with col4:
                st.metric("🧂 혈청나트륨", f"{st.session_state.user_data.get('serum_sodium', 0)} mEq/L")
            
            st.divider()
            
            # 데이터셋과 비교 (인터랙티브 그래프)
            st.markdown("### 📈 집단 데이터와의 비교")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 나이별 사망 위험도
                fig_age = px.scatter(
                    df2,
                    x='age',
                    y='DEATH_EVENT',
                    color='DEATH_EVENT',
                    size='ejection_fraction',
                    hover_data=['creatinine_phosphokinase', 'serum_creatinine'],
                    color_discrete_map={0: '#6BCB77', 1: '#FF6B6B'},
                    title="나이별 사망 위험도 분포",
                    labels={'DEATH_EVENT': '사망 여부', 'age': '나이 (세)'}
                )
                fig_age.add_vline(
                    x=st.session_state.user_age,
                    line_dash="dash",
                    line_color="blue",
                    annotation_text=f"당신: {st.session_state.user_age}세"
                )
                st.plotly_chart(fig_age, use_container_width=True)
            
            with col2:
                # 심박수와 혈압의 관계
                fig_scatter = px.scatter(
                    df2,
                    x='serum_creatinine',
                    y='ejection_fraction',
                    color='DEATH_EVENT',
                    color_discrete_map={0: '#6BCB77', 1: '#FF6B6B'},
                    title="혈청 크레아티닌 vs 박출률",
                    labels={'serum_creatinine': '혈청 크레아티닌', 'ejection_fraction': '박출률 (%)'}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # 예측 모델의 중요도
            st.markdown("### 🎯 영향도 높은 요인 TOP 5")
            
            feature_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': model.feature_importances_
            }).sort_values('Importance', ascending=False).head(5)
            
            fig_importance = px.bar(
                feature_importance,
                x='Importance',
                y='Feature',
                orientation='h',
                title="사망 위험도 예측에 영향을 주는 상위 5가지 요인",
                color='Importance',
                color_continuous_scale='Reds'
            )
            fig_importance.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_importance, use_container_width=True)
        
        else:
            st.warning("⚠️ 먼저 '나의 상태 점검'에서 정보를 입력해주세요!")
    
    # ==================== TAB 3: Community ====================
    with tab3:
        st.markdown("### 👥 심부전 환자 커뮤니티")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 사망 여부 분포")
            death_counts = df2['DEATH_EVENT'].value_counts()
            fig_death = go.Figure(data=[
                go.Bar(
                    x=['생존', '사망'],
                    y=[death_counts[0], death_counts[1]],
                    marker=dict(color=['#6BCB77', '#FF6B6B']),
                    text=[death_counts[0], death_counts[1]],
                    textposition='auto'
                )
            ])
            fig_death.update_layout(
                title_text="전체 환자의 예후",
                xaxis_title="",
                yaxis_title="환자 수",
                height=400
            )
            st.plotly_chart(fig_death, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎂 나이 분포")
            fig_age_dist = px.histogram(
                df2,
                x='age',
                nbins=20,
                title="환자 나이 분포",
                color_discrete_sequence=['#4D96FF'],
                labels={'age': '나이 (세)', 'count': '환자 수'}
            )
            st.plotly_chart(fig_age_dist, use_container_width=True)
        
        # 통계 정보
        st.markdown("---")
        st.markdown("### 📈 통계 요약")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 총 환자 수", len(df2))
        with col2:
            st.metric("💀 사망률", f"{(df2['DEATH_EVENT'].sum()/len(df2)*100):.1f}%")
        with col3:
            st.metric("🎂 평균 나이", f"{df2['age'].mean():.0f}세")
        with col4:
            st.metric("💓 평균 박출률", f"{df2['ejection_fraction'].mean():.0f}%")

# ========== 페이지2: 건강 정보 ==========
else:
    st.image(r"D:\bootcamp\bootcamp_train\img.png", width=120)
    st.markdown("# 💚 건강 정보를 공유해요!")
    st.markdown("*심부전에 대한 정보와 예방법을 알아봅시다*")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 심부전이란?")
        st.write("""
        **심부전(Heart Failure)**은 심장이 신체에 필요한 혈액을 충분히 펌프질하지 못하는 상태입니다.
        
        주요 증상:
        - 호흡 곤란
        - 피로감
        - 다리 부종
        - 야간 빈뇨
        """)
    
    with col2:
        st.markdown("### ⚠️ 위험 요소")
        st.write("""
        심부전의 주요 원인:
        - 🫀 고혈압
        - 🩸 당뇨병
        - 🚬 흡연
        - 🧬 높은 콜레스테롤
        - 👨‍👩‍👧‍👦 가족력
        """)
    
    st.divider()
    
    st.markdown("### 📊 실시간 데이터 분석")
    
    # 인터랙티브 필터
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_age = st.slider("최소 나이", min_value=0, max_value=100, value=20)
    with col2:
        max_age = st.slider("최대 나이", min_value=0, max_value=100, value=100)
    with col3:
        show_death = st.checkbox("사망 환자만 표시", value=False)
    
    # 필터링된 데이터
    filtered_df = df2[
        (df2['age'] >= min_age) & 
        (df2['age'] <= max_age)
    ]
    
    if show_death:
        filtered_df = filtered_df[filtered_df['DEATH_EVENT'] == 1]
    
    # 필터링된 데이터로 그래프 그리기
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter = px.scatter(
            filtered_df,
            x='age',
            y='serum_creatinine',
            color='DEATH_EVENT',
            color_discrete_map={0: '#6BCB77', 1: '#FF6B6B'},
            title=f"나이별 혈청 크레아티닌 (n={len(filtered_df)})",
            labels={'serum_creatinine': '혈청 크레아티닌', 'DEATH_EVENT': '사망 여부'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_box = px.box(
            filtered_df,
            x='DEATH_EVENT',
            y='ejection_fraction',
            color='DEATH_EVENT',
            color_discrete_map={0: '#6BCB77', 1: '#FF6B6B'},
            title="박출률 분포",
            labels={'ejection_fraction': '박출률 (%)', 'DEATH_EVENT': '사망 여부'}
        )
        fig_box.update_xaxes(ticktext=['생존', '사망'], tickvals=[0, 1])
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 💊 예방 및 관리")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🏃 생활 습관
        - 규칙적인 운동
        - 스트레스 관리
        - 충분한 수면
        - 금연, 금주
        """)
    
    with col2:
        st.markdown("""
        #### 🍎 식생활
        - 저염식 식단
        - 포화지방 제한
        - 신선한 과일/채소
        - 수분 섭취 조절
        """)
    
    with col3:
        st.markdown("""
        #### 🏥 의료 관리
        - 정기 검진
        - 혈압 모니터링
        - 약물 복용
        - 의사와 상담
        """)

# ========== 하단 푸터 ==========
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>💓 심부전 환자 분석 대시보드 v2.0 | 2026.06.25</p>
    <p>⚠️ 이 정보는 의료 전문가 상담을 대체할 수 없습니다. 질문이 있으시면 담당 의사와 상담하세요.</p>
</div>
""", unsafe_allow_html=True)
