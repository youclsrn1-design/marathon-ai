import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. 페이지 및 브랜딩 설정 (와이드 모드)
st.set_page_config(page_title="MARATHON AI | PRO Analytics", layout="wide", initial_sidebar_state="expanded")

# 2. 하이엔드 대시보드 전용 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #f0f2f6; }
    
    .header-panel {
        background: linear-gradient(135deg, #0A192F 0%, #002D62 100%);
        padding: 40px 30px; border-radius: 20px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; align-items: center; justify-content: space-between;
    }
    .title-box h1 { margin: 0; font-size: 2.5em; font-weight: 900; letter-spacing: -1px; }
    .title-box p { margin: 5px 0 0 0; color: #8892B0; font-size: 1.1em; letter-spacing: 1px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; border-bottom: 3px solid #CD2E3A !important; font-weight: bold; color: #002D62 !important; }
    
    .data-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; height: 100%;
    }
    .highlight-red { color: #CD2E3A; font-weight: 700; }
    .highlight-blue { color: #0047A0; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. 상단 헤더 패널
st.markdown("""
    <div class="header-panel">
        <div class="title-box">
            <h1>🇰🇷 MARATHON AI PRO</h1>
            <p>Advanced Biometric & Gait Analysis Dashboard</p>
        </div>
        <div style="text-align: right;">
            <span style="background: #CD2E3A; padding: 5px 15px; border-radius: 20px; font-size: 0.9em; font-weight: bold;">Toss ID: MARATHON AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. 사이드바 (입력 컨트롤)
with st.sidebar:
    st.markdown("### 🎥 비전 데이터 입력")
    video_file = st.file_uploader("러닝 영상 업로드", type=['mp4', 'mov'])
    
    st.markdown("---")
    st.markdown("### ⚙️ 분석 파라미터")
    gender = st.selectbox("성별", ["남성 (Male)", "여성 (Female)"])
    target_group = st.selectbox("비교 벤치마크", 
        ["세계 신기록 보유자 (World Record)", "글로벌 TOP 10 평균", "대한민국 국가대표 평균"])
    
    st.markdown("---")
    analyze_btn = st.button("🚀 정밀 역학 분석 실행", use_container_width=True)

# 5. 메인 분석 영역
if video_file is not None and analyze_btn:
    with st.spinner('AI 딥러닝 비전 엔진이 120개 관절 프레임을 정밀 추적 중입니다...'):
        # 가상 분석 데이터 (실제 분석 알고리즘 대체)
        score = 82
        metrics_categories = ['무릎 신전(Extension)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 안정성(Pelvic)', '케이던스(SPM)']
        my_stats = [75, 68, 85, 70, 80]
        world_stats = [98, 95, 96, 99, 97]
        korea_stats = [85, 88, 80, 85, 90]
        
        u_angle = np.random.normal(159, 3.5, 100)
        
    # 탭 구성 (시각화/데이터/솔루션 분리)
    tab1, tab2, tab3 = st.tabs(["📊 다차원 종합 지표", "📐 관절 역학 그래프", "💡 바이오메카닉 솔루션"])
    
    with tab1:
        colA, colB = st.columns([1, 1.5])
        with colA:
            st.markdown('<div class="data-card">', unsafe_allow_html=True)
            st.markdown("#### 🏆 종합 퍼포먼스 스코어")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Overall Biometric Score", 'font': {'size': 16}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#0047A0"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ffe6e6"},
                        {'range': [60, 85], 'color': "#e6f2ff"},
                        {'range': [85, 100], 'color': "#e6ffe6"}],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}
                }))
            fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with colB:
            st.markdown('<div class="data-card">', unsafe_allow_html=True)
            st.markdown("#### 🕸️ 5대 역학 지표 벤치마크 (Radar Chart)")
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=metrics_categories, fill='toself', name='내 데이터', line_color='#CD2E3A'))
            fig_radar.add_trace(go.Scatterpolar(r=world_stats, theta=metrics_categories, fill='none', name='World Record Target', line_color='#0047A0', line_dash='dash'))
            fig_radar.add_trace(go.Scatterpolar(r=korea_stats, theta=metrics_categories, fill='none', name='Korea Elite', line_color='#888', line_dash='dot'))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=350, margin=dict(l=40, r=40, t=30, b=20))
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 프레임별 무릎 관절 가동성 (Kinematic Tracking)")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(y=u_angle, name='내 실시간 각도', line=dict(color='#CD2E3A', width=3)))
        fig_line.add_trace(go.Scatter(y=[168.5]*100, name='World Record (168.5°)', line=dict(color='#0047A0', dash='dash')))
        fig_line.add_trace(go.Scatter(y=[162.8]*100, name='Korea Elite (162.8°)', line=dict(color='#999', dash='dot')))
        fig_line.update_layout(xaxis_title='분석 프레임 (Frame)', yaxis_title='무릎 신전 각도 (Degree)', height=400, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        colC, colD = st.columns([1, 1])
        with colC:
            st.markdown('<div class="data-card">', unsafe_allow_html=True)
            st.markdown("#### 🔬 분석 요약 (Diagnostic Summary)")
            st.markdown("""
            레이더 차트 분석 결과, 귀하의 러닝 폼은 **'수직 진폭(Oscillation)'**과 **'케이던스(SPM)'** 부문에서는 우수한 수치를 보이고 있으나, 
            <span class="highlight-red">지면 접촉 시간(GCT)</span>과 <span class="highlight-red">무릎 신전(Extension)</span>에서 글로벌 엘리트 대비 심각한 에너지 누수가 발생하고 있습니다.
            <br><br>
            이는 착지 시 브레이킹 포스(Braking Force)가 크게 작용하여 전진 관성을 갉아먹는 전형적인 **'오버스트라이드(Overstride)'** 형태입니다.
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with colD:
            st.markdown('<div class="data-card">', unsafe_allow_html=True)
            st.markdown("#### 🛠️ 전문 교정 프로토콜 (Actionable Plan)")
            st.markdown("""
            1. <span class="highlight-blue">착지점 재조정 (Mid-foot Strike):</span> 발이 몸의 무게중심보다 과도하게 앞에 떨어지지 않도록 보폭을 줄이고 케이던스를 5% 높이세요.
            2. <span class="highlight-blue">장요근/둔근 활성화:</span> 도약기에서 엉덩이 근육을 사용하여 지면을 끝까지 밀어내는 'Push-off' 훈련을 주 2회 추가해야 합니다.
            3. <span class="highlight-blue">골반 틸트 교정:</span> 골반이 뒤로 빠진 상태(후방경사)에서는 무릎을 160도 이상 펴기 어렵습니다. 코어 긴장을 유지하며 골반을 중립으로 세우세요.
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
        <div style='text-align: center; padding: 100px 20px; background: white; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>
            <h2 style='font-size: 2.5em; color: #002D62; margin-bottom: 10px;'>High-Performance AI Running Coach</h2>
            <p style='font-size: 1.2em; color: #666; margin-bottom: 30px;'>좌측 사이드바에 영상을 업로드하고, 세계 최고 수준의 생체역학 정밀 분석을 경험하세요.</p>
            <div style='display: flex; justify-content: center; gap: 30px; opacity: 0.6;'>
                <div>📊 다차원 지표 분석</div>
                <div>📐 관절 각도 트래킹</div>
                <div>💡 맞춤형 교정 솔루션</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

