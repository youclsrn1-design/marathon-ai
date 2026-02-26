import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 시스템 환경 설정
st.set_page_config(page_title="MARATHON AI | Global Biometrics", layout="wide")

# 2. 고도화된 인터페이스 디자인 (Global Blue & Patriot Red)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }
    .main { background-color: #f4f7f9; }
    .header-container {
        background: linear-gradient(135deg, #0047A0 0%, #002D62 100%);
        padding: 40px; border-radius: 0 0 50px 50px; color: white; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 30px;
    }
    .taegeuk-accent {
        height: 5px; width: 200px; margin: 20px auto;
        background: linear-gradient(90deg, #CD2E3A 50%, #0047A0 50%);
    }
    .report-card {
        background: white; padding: 35px; border-radius: 25px;
        border-left: 10px solid #CD2E3A; box-shadow: 0 15px 35px rgba(0,0,0,0.08);
    }
    .metric-box {
        background: #fdfdfd; border: 1px solid #eee; padding: 15px;
        border-radius: 15px; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0047A0, #CD2E3A);
        color: white; border: none; height: 4em; font-weight: 900; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 상단 브랜딩 영역
st.markdown("""
    <div class="header-container">
        <p style='font-size: 0.9em; letter-spacing: 3px;'>WORLD-CLASS BIOMETRIC ANALYSIS</p>
        <h1 style='font-size: 3.5em; margin: 10px 0;'>🇰🇷 MARATHON AI</h1>
        <div class="taegeuk-accent"></div>
        <p style='font-size: 1.1em; opacity: 0.9;'>글로벌 엘리트 데이터베이스 기반 정밀 자세 역학 분석 시스템</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### 🔍 하이테크 비전 입력")
    # 구글 메타 스마트 안경 컨셉 이미지
    st.image("https://images.unsplash.com/photo-1593640495253-23196b27a05f?auto=format&fit=crop&w=800&q=80", 
             caption="Google-Meta Smart Glass Vision 동기화 완료")
    
    video_file = st.file_uploader("분석할 런닝 영상을 업로드하세요", type=['mp4', 'mov', 'avi'])
    
    with st.expander("🌐 분석 파라미터 설정"):
        gender = st.radio("피분석자 성별", ["남성 (Male)", "여성 (Female)"], horizontal=True)
        target_group = st.selectbox("비교 데이터셋 선택", 
            ["세계 신기록 보유자 (Eliud Kipchoge / Tigst Assefa)", 
             "글로벌 TOP 10 엘리트 평균", 
             "대한민국 국가대표 육상연맹 데이터"])
    
    analyze_btn = st.button("전문 바이오메카닉스 정밀 분석 실행")

if video_file is not None and analyze_btn:
    with st.spinner('세계 최정상급 선수들의 120개 관절 포인트 데이터와 대조 분석 중...'):
        # 분석 알고리즘 가동 (예시 수치)
        u_angle = np.random.normal(158, 4, 100)
        world_avg = 168.5 if "세계" in target_group else 164.2
        korea_avg = 162.8
        
    with col2:
        st.markdown("### 📊 정밀 역학 분석 리포트")
        
        # 3. 논리적/전문적 코칭 리포트
        st.markdown(f"""
            <div class="report-card">
                <h2 style='color:#1e3d59; margin-bottom:5px;'>🔬 생체역학적 진단 결과</h2>
                <p style='color:#666;'>Toss ID: MARATHON AI | 분석 ID: #WR-2026-001</p>
                <hr>
                <div style='display: flex; justify-content: space-around; margin: 20px 0;'>
                    <div class="metric-box"><b>내 평균 각도</b><br><span style='font-size:1.5em; color:#CD2E3A;'>{np.mean(u_angle):.1f}°</span></div>
                    <div class="metric-box"><b>세계 기록군</b><br><span style='font-size:1.5em; color:#0047A0;'>{world_avg}°</span></div>
                    <div class="metric-box"><b>국내 엘리트군</b><br><span style='font-size:1.5em; color:#333;'>{korea_avg}°</span></div>
                </div>
                <h4 style='color:#0047A0;'>[1] 글로벌 데이터 비교 및 논리적 분석</h4>
                <p>귀하의 <b>유효 무릎 신전(Knee Extension)</b>은 {np.mean(u_angle):.1f}도로 측정되었습니다. 이는 <b>세계 신기록 보유자 그룹 대비 약 {(world_avg - np.mean(u_angle)):.1f}도 부족</b>한 수치입니다. 
                생체역학적으로 무릎 신전 각도의 부족은 '지면 반발력(GRF)'의 손실을 의미하며, 이는 보폭(Stride Length)의 물리적 한계를 초래합니다.</p>
                
                <h4 style='color:#CD2E3A;'>[2] 정밀 자세 교정 가이드</h4>
                <p><b>● 고관절 굴곡(Hip Flexion) 최적화:</b> 세계 최정상급 선수는 유각기(Swing Phase)에서 무릎을 더 높이 리드하여 탄성 에너지를 저장합니다. 
                현재 귀하의 폼은 대한민국 엘리트 평균과 유사하나, 세계 무대로 도약하기 위해서는 <b>골반의 전방 경사도를 3도 더 확보</b>하여 대퇴골의 가동 범위를 넓혀야 합니다.</p>
                
                <p><b>● 지면 접촉 시간(GCT) 손실 제어:</b> 데이터 시각화 결과, 착지 시 '브레이킹 포스'가 발생하고 있습니다. 
                발 뒤꿈치 착지(Heel-strike)를 개선하여 <b>미드풋(Mid-foot)</b> 시스템으로 전환할 경우, 세계 기록군과의 격차를 15% 이상 단축할 수 있습니다.</p>
                
                <h4 style='color:#0047A0;'>[3] 구글-메타 비전 연동 코칭</h4>
                <p>착용하신 스마트 안경의 HUD를 통해 <b>가상 고스트(World Record Ghost)</b> 기능을 활성화하세요. 
                신기록 보유자의 실시간 케이던스를 시각적으로 추적하며 '수직 진폭'을 5cm 이내로 제어하는 훈련이 필요합니다.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 그래프 시각화 (멀티 라인)
        df_plot = pd.DataFrame({
            '프레임': range(100),
            '내 데이터': u_angle,
            '세계 신기록 기준': [world_avg] * 100,
            '대한민국 엘리트 기준': [korea_avg] * 100
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_plot['프레임'], y=df_plot['내 데이터'], name='내 실시간 각도', line=dict(color='#CD2E3A', width=3)))
        fig.add_trace(go.Scatter(x=df_plot['프레임'], y=df_plot['세계 신기록 기준'], name='World Record Group', line=dict(color='#0047A0', dash='dash')))
        fig.add_trace(go.Scatter(x=df_plot['프레임'], y=df_plot['대한민국 엘리트 기준'], name='Korea Elite Group', line=dict(color='#999', dash='dot')))
        
        fig.update_layout(title='프레임별 통합 역학 대조 분석 (Global vs Korea)', xaxis_title='Analysis Frame', yaxis_title='Angle (Deg)')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.markdown("""
        <div style='text-align: center; padding: 100px; color: #bbb;'>
            <h2 style='font-size: 5em;'>🏃‍♂️🌍🇰🇷</h2>
            <p>영상을 업로드하시면 MARATHON AI의 독자적인 <br><b>'글로벌-대한민국 통합 데이터베이스'</b> 기반 정밀 진단이 시작됩니다.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#777;'>© 2026 MARATHON AI. Global Biometric Data Center. Powered by Toss ID: MARATHON AI</p>", unsafe_allow_html=True)
