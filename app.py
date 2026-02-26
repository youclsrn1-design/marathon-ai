import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 (브라우저 탭에 표시될 이름)
st.set_page_config(page_title="MARATHON AI - 정밀 분석 코치", layout="wide", initial_sidebar_state="collapsed")

# 2. 파랑/빨강/태극기 테마 디자인 (CSS)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .main { background-color: #f8f9fa; }
    
    /* 태극기 상단 바 디자인 */
    .header-bar {
        background: linear-gradient(90deg, #0047A0 50%, #CD2E3A 50%);
        height: 10px;
        width: 100%;
        margin-bottom: 20px;
    }
    
    /* 타이틀 스타일 */
    .main-title {
        color: #1e3d59;
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }

    /* 버튼 스타일 (토스 느낌의 세련된 블루) */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #0047A0;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #CD2E3A; /* 호버 시 빨간색으로 변신 */
        transform: translateY(-2px);
    }

    /* 리포트 카드 스타일 */
    .report-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border-top: 5px solid #0047A0;
    }
    
    .highlight { color: #CD2E3A; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 상단 태극 테마 바
st.markdown('<div class="header-bar"></div>', unsafe_allow_html=True)

# 3. 서비스 로고 및 타이틀
st.markdown('<h1 class="main-title">🇰🇷 MARATHON AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">국가대표급 정밀 분석 시스템 | Toss ID: MARATHON AI</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎥 AI 정밀 트래킹")
    # 구글/메타 스마트 안경 컨셉 이미지
    st.image("https://images.unsplash.com/photo-1593640495253-23196b27a05f?auto=format&fit=crop&w=800&q=80", 
             caption="Google-Meta Smart Glass 기반 실시간 데이터 연동 시뮬레이션")
    
    video_file = st.file_uploader("분석할 영상을 업로드하세요", type=['mp4', 'mov', 'avi'])
    
    st.info("💡 Tip: 측면에서 촬영된 영상일수록 분석 정확도가 높아집니다.")
    analyze_btn = st.button("전문 AI 정밀 분석 시작")

if video_file is not None and analyze_btn:
    with st.spinner('국가대표 분석 엔진이 관절 좌표를 계산 중입니다...'):
        # 가상 분석 데이터 생성 (실제 구현 시 MediaPipe 결과값 적용)
        mock_data = np.random.normal(loc=162, scale=8, size=60)
        
    with col2:
        st.markdown('### 📊 MARATHON AI 분석 리포트')
        
        # 전문적인 코칭 섹션
        st.markdown(f"""
            <div class="report-card">
                <h2 style='color:#0047A0;'>🏃‍♂️ 정밀 분석 결과</h2>
                <hr>
                <p><b>1. 무릎 가동 범위:</b> <span class="highlight">{np.mean(mock_data):.1f}°</span> (정상 범위: 155~165°)</p>
                <p><b>2. 지면 접촉 시간(GCT):</b> <span class="highlight">195ms</span> (엘리트 기준: 180ms 이하)</p>
                <hr>
                <h3 style='color:#CD2E3A;'>📋 전문가 코칭 가이드</h3>
                <p><b>[현재 문제점]</b><br>
                분석 결과, 착지 시 무릎이 과하게 펴지는 '오버스트라이드' 현상이 관찰됩니다. 이는 무릎 연골에 가해지는 충격을 1.5배 높이며 피로 골절의 원인이 될 수 있습니다.</p>
                <p><b>[솔루션 제안]</b><br>
                1. <b>착지점 수정:</b> 발뒤꿈치가 몸보다 멀리 나가지 않도록 <b>무게중심 바로 아래</b>에 발을 딛으세요.<br>
                2. <b>골반 회전:</b> 골반의 가동 범위를 5도만 더 넓히면 보폭을 줄이지 않고도 효율적인 착지가 가능합니다.<br>
                3. <b>보강 운동:</b> 대퇴이두근(허벅지 뒤쪽) 근력이 부족합니다. 주 2회 햄스트링 컬 운동을 권장합니다.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 분석 그래프
        fig = px.line(x=range(len(mock_data)), y=mock_data, 
                      title="러닝 사이클별 관절 각도 정밀 추이",
                      labels={'x':'프레임(Frame)', 'y':'각도(Degree)'},
                      color_discrete_sequence=['#0047A0'])
        st.plotly_chart(fig, use_container_width=True)

else:
    with col2:
        st.markdown("""
            <div style='text-align: center; padding-top: 100px; color: #aaa;'>
                <p style='font-size: 5rem;'>🇰🇷</p>
                <p>영상을 업로드하면 대한민국 1% 엘리트 데이터와 비교한<br>전문 코칭 리포트가 생성됩니다.</p>
            </div>
            """, unsafe_allow_html=True)

# 하단 푸터
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>© 2026 MARATHON AI. All Rights Reserved. | Powered by Google Meta Vision</p>", unsafe_allow_html=True)
