import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# 1. 시스템 설정
st.set_page_config(page_title="MARATHON AI | PRO", layout="wide", initial_sidebar_state="expanded")

# 2. 하이엔드 대시보드 & 프린트 최적화 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #f4f7f9; }
    
    /* 화면용 화려한 디자인 */
    .header-panel {
        background: linear-gradient(135deg, #0A192F 0%, #002D62 100%);
        padding: 40px 30px; border-radius: 20px; color: white; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center;
    }
    .data-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; height: 100%;
    }
    .feedback-box {
        background: white; padding: 30px; border-radius: 15px; margin-top: 40px;
        border-top: 5px solid #CD2E3A; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }
    .highlight-red { color: #CD2E3A; font-weight: 700; }
    
    /* 인쇄(프린트) 전용 깔끔한 세팅 */
    @media print {
        .no-print, section[data-testid="stSidebar"], .feedback-box, .stTabs [data-baseweb="tab-list"], button { display: none !important; }
        body { background-color: white !important; }
        .header-panel { background: white !important; color: black !important; box-shadow: none !important; border-bottom: 3px solid #002D62; border-radius: 0; padding: 20px 0; }
        .data-card { border: 2px solid #333 !important; box-shadow: none !important; page-break-inside: avoid; margin-bottom: 20px; }
        h1 { color: #002D62 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 메인 헤더
st.markdown("""
    <div class="header-panel">
        <div>
            <h1 style='margin:0; font-weight:900; font-size:2.5em;'>🇰🇷 MARATHON AI PRO</h1>
            <p style='margin:5px 0 0 0; color:#8892B0;'>Global Biometric Performance & Gait Analysis</p>
        </div>
        <div class="no-print">
            <span style="background: #CD2E3A; padding: 8px 20px; border-radius: 20px; font-weight: bold;">Toss ID: MARATHON AI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. 사이드바 (입력 컨트롤)
with st.sidebar:
    st.markdown("### 🎥 비전 데이터 입력")
    video_file = st.file_uploader("러닝 영상 업로드", type=['mp4', 'mov'])
    gender = st.selectbox("성별", ["남성 (Male)", "여성 (Female)"])
    target_group = st.selectbox("비교 벤치마크", ["세계 신기록 보유자", "글로벌 TOP 10 평균", "대한민국 국가대표"])
    analyze_btn = st.button("🚀 정밀 역학 분석 실행", use_container_width=True)
    
    st.markdown("---")
    st.info("🖨️ **리포트 출력:** 분석 완료 후 `Ctrl + P` (Mac은 `Cmd + P`)를 누르면 A4 용지에 맞게 깔끔하게 인쇄됩니다.")

# 5. 분석 로직 및 시각화 영역
if video_file and analyze_btn:
    with st.spinner('세계 최정상급 선수의 120개 관절 프레임과 대조 중...'):
        # 가상 데이터 생성
        score = 82
        metrics_categories = ['무릎 신전(Extension)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 안정성(Pelvic)', '케이던스(SPM)']
        my_stats = [75, 68, 85, 70, 80]
        world_stats = [98, 95, 96, 99, 97]
        u_angle = np.random.normal(159, 3.5, 100)
        
    st.markdown("<h3 class='no-print'>📊 생체역학 정밀 진단 리포트</h3>", unsafe_allow_html=True)
    
    # 상단 2분할 (게이지 차트 & 레이더 차트)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown("#### 🏆 종합 역학 스코어")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=score, domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0047A0"},
                   'steps': [{'range': [0, 60], 'color': "#ffe6e6"}, {'range': [60, 85], 'color': "#e6f2ff"}, {'range': [85, 100], 'color': "#e6ffe6"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown("#### 🕸️ 5대 역학 지표 벤치마크 (vs World Record)")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=metrics_categories, fill='toself', name='내 데이터', line_color='#CD2E3A'))
        fig_radar.add_trace(go.Scatterpolar(r=world_stats, theta=metrics_categories, fill='none', name='World Record Target', line_color='#0047A0', line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=40, r=40, t=30, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 하단 2분할 (라인 그래프 & 솔루션)
    col3, col4 = st.columns([1.5, 1])
    with col3:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown("#### 📈 프레임별 무릎 관절 가동성 (Kinematic Tracking)")
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(y=u_angle, name='내 실시간 각도', line=dict(color='#CD2E3A', width=3)))
        fig_line.add_trace(go.Scatter(y=[168.5]*100, name='World Record (168.5°)', line=dict(color='#0047A0', dash='dash')))
        fig_line.update_layout(xaxis_title='Analysis Frame', yaxis_title='Angle (Degree)', height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 전문 교정 프로토콜")
        st.markdown(f"""
        **1. 지면 반발력(GRF) 누수 제어**
        현재 무릎 신전 각도는 평균 <span class="highlight-red">{np.mean(u_angle):.1f}°</span>로 세계 기록군 대비 약 9.5° 부족합니다. 도약 시 브레이킹 포스가 발생하고 있습니다.
        
        **2. 착지점 재조정 (Mid-foot Strike)**
        발이 무게중심보다 과도하게 앞에 떨어지지 않도록 케이던스를 5% 높이세요.
        
        **3. 골반 틸트 교정**
        코어 긴장을 유지하며 골반을 중립으로 세워 대퇴골의 가동 범위를 확보해야 합니다.
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. 고객 검증용 피드백 섹션 (프린트 시에는 안 보임)
    st.markdown('<div class="feedback-box no-print">', unsafe_allow_html=True)
    st.markdown("### 💬 MVP 고객 검증 피드백 (예창패 제출용)")
    st.write("본 서비스는 예비창업패키지 선정을 위한 베타 테스트 중입니다. 런닝 폼 분석 결과에 대한 자유로운 의견을 남겨주시면 큰 힘이 됩니다.")
    
    with st.form("feedback_form", clear_on_submit=True):
        f_name = st.text_input("소속 및 성함 (예: 마라톤동호회 홍길동 / 일반 러너)")
        f_comment = st.text_area("분석 리포트가 런닝 자세 교정에 도움이 되셨나요? 추가되었으면 하는 기능이 있다면 적어주세요.")
        f_submit = st.form_submit_button("피드백 데이터 전송")
        
        if f_submit and f_comment:
            st.success(f"감사합니다! 남겨주신 소중한 데이터는 MARATHON AI의 서비스 고도화 및 투자 유치 자료로 활용됩니다.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("좌측 사이드바에 영상을 업로드하고, 세계 최고 수준의 생체역학 정밀 분석을 경험하세요.")

st.markdown("<p style='text-align:center; color:silver; font-size:0.8em; margin-top:50px;'>© 2026 MARATHON AI. Powered by Toss ID: MARATHON AI</p>", unsafe_allow_html=True)
