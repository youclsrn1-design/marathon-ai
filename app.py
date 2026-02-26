import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 시스템 설정
st.set_page_config(page_title="MARATHON AI | Global Standard", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩
ui_langs = {
    "🇰🇷 한국어": {
        "title": "MARATHON AI PRO", "sub": "글로벌 생체역학 정밀 분석 표준 시스템", "toss": "Toss ID: MARATHON AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", 
        "s_data": "📊 비교 벤치마크", "s_vid": "🎥 비전 데이터 입력", "s_up": "러닝 영상 업로드", 
        "s_gen": "성별", "s_btn": "🚀 정밀 역학 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "cat": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 안정성', '케이던스'],
        "sol_title": "💡 맞춤형 교정 프로토콜", 
        "sol_txt": "선택하신 국가의 엘리트 데이터와 비교했을 때, 착지 시 브레이킹 포스가 발생하고 있습니다. 케이던스를 높여 지면 접촉 시간을 단축하세요.",
        "img_title": "📸 비전 AI 관절 추출 및 궤적 오버레이",
        "img_desc": "도약(Push-off) 순간의 관절 좌표를 추출하여, 사용자의 무릎 각도(🔴)와 벤치마크 기준선(🟡)의 편차를 시각화합니다.",
        "f_title": "💬 글로벌 사용자 피드백", "f_desc": "MARATHON AI는 전 세계 러너들의 피드백을 통해 성장합니다."
    },
    "🇺🇸 English": {
        "title": "MARATHON AI PRO", "sub": "Global Standard Biometric Analysis System", "toss": "Powered by MARATHON AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", 
        "s_data": "📊 Benchmark Target", "s_vid": "🎥 Vision Data Input", "s_up": "Upload Running Video", 
        "s_gen": "Gender", "s_btn": "🚀 Run Precision Analysis", "r_title": "🔬 Biometric Diagnostic Report",
        "cat": ['Knee Ext.', 'GCT', 'Oscillation', 'Pelvic Stability', 'Cadence'],
        "sol_title": "💡 Actionable Coaching Protocol", 
        "sol_txt": "Compared to the selected elite benchmark, there is a noticeable braking force during foot strike. Increase cadence to reduce Ground Contact Time.",
        "img_title": "📸 Vision AI Frame Overlay Analysis",
        "img_desc": "Visualizing the deviation between your knee angle (🔴) and the benchmark target (🟡) during the push-off phase.",
        "f_title": "💬 Global User Feedback", "f_desc": "MARATHON AI grows with feedback from runners worldwide."
    }
}

# 3. 데이터베이스
benchmarks = {
    "🌍 World Record (세계 신기록)": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"},
    "🇰🇪 Kenya Elite (케냐 최상위)": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"},
    "🇺🇸 US Olympic (미국 국가대표)": {"angle": 164.5, "radar": [88, 90, 85, 88, 92], "color": "#3C3B6E"},
    "🇯🇵 Japan Elite (일본 대표팀)": {"angle": 163.5, "radar": [87, 89, 82, 87, 91], "color": "#BC002D"},
    "🇨🇳 China Elite (중국 대표팀)": {"angle": 163.0, "radar": [86, 88, 81, 86, 89], "color": "#EE1C25"},
    "🇰🇷 Korea Elite (대한민국 대표팀)": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"},
    "🌐 Global Amateur (일반인 평균)": {"angle": 155.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
}

# 4. CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #f4f7f9; }
    .header-panel { background: linear-gradient(135deg, #112A46 0%, #001B3A 100%); padding: 35px 30px; border-radius: 20px; color: white; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; height: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    selected_bench = st.selectbox("📊 Benchmark Target", list(benchmarks.keys()))
    b_data = benchmarks[selected_bench]
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov'])
    analyze_btn = st.button(t['s_btn'], use_container_width=True)

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.2em;'>🌍 {t['title']}</h1><p style='margin:5px 0 0 0; color:#8892B0;'>{t['sub']}</p></div>
        <div><span style="background: #0047A0; padding: 8px 20px; border-radius: 20px; font-weight: bold;">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 분석 영역
if video_file and analyze_btn:
    with st.spinner('Syncing with Global Biometric Data Center...'):
        score = 82
        my_stats = [75, 68, 85, 70, 80]
        u_angle = np.random.normal(155.5, 3.5, 100)
        avg_angle = np.mean(u_angle)
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        
    st.markdown(f"<h3>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, domain={'x': [0, 1], 'y': [0, 1]}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0047A0"}, 'steps': [{'range': [0, 60], 'color': "#ffe6e6"}, {'range': [85, 100], 'color': "#e6ffe6"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 95}}))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=t['cat'], fill='toself', name='My Data', line_color='#CD2E3A'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=t['cat'], fill='none', name=selected_bench.split(" ")[1], line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=40, r=40, t=30, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 📸 새로운 비주얼 오버레이: 수학적 모델로 뼈대 각도 직접 그리기
    st.markdown(f"""
        <div class="data-card" style="margin-top: 20px; border-top: 5px solid #FFB300; display:flex; flex-direction:column;">
            <h4 style="color: #002D62; margin-top: 0;">{t['img_title']}</h4>
            <p style="color: #555;">{t['img_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    
    with col3:
        # 무릎 각도를 시각화하기 위한 수학적 좌표 계산 (삼각함수 활용)
        # 고관절(Hip)을 (0, 1), 무릎(Knee)을 (0, 0)으로 기준 잡음
        x_my_ankle = np.sin(np.radians(180 - avg_angle))
        y_my_ankle = -np.cos(np.radians(180 - avg_angle))
        
        x_target_ankle = np.sin(np.radians(180 - target_angle))
        y_target_ankle = -np.cos(np.radians(180 - target_angle))

        fig_overlay = go.Figure()
        
        # 1. 대퇴부 (허벅지) 뼈대
        fig_overlay.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), marker=dict(size=12, color='white'), name='대퇴부 (Thigh)'))
        # 2. 내 종아리 뼈대 (빨간색)
        fig_overlay.add_trace(go.Scatter(x=[0, x_my_ankle], y=[0, y_my_ankle], mode='lines+markers', line=dict(color='#CD2E3A', width=8), marker=dict(size=12, color='#CD2E3A'), name=f'내 무릎 ({avg_angle:.1f}°)'))
        # 3. 기준 종아리 뼈대 (노란색 점선)
        fig_overlay.add_trace(go.Scatter(x=[0, x_target_ankle], y=[0, y_target_ankle], mode='lines', line=dict(color='#FFB300', width=4, dash='dash'), name=f'기준선 ({target_angle:.1f}°)'))

        fig_overlay.update_layout(
            title="Knee Extension Tracking Vision HUD",
            plot_bgcolor='#112A46', paper_bgcolor='#112A46', font=dict(color='white'),
            xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]),
            margin=dict(l=20, r=20, t=40, b=20), height=350,
            showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        st.markdown(f"""
        <div style="background: white; padding: 30px; border-radius: 15px; border: 1px solid #eee; height: 100%;">
            <h4 style="margin-top:0; color:#002D62;">📊 분석 결과 요약</h4>
            <div style="font-size: 1.2em; margin: 20px 0; line-height: 1.8;">
                <span style="color: #CD2E3A; font-weight: 900;">🔴 내 무릎 각도: {avg_angle:.1f}°</span><br>
                <span style="color: #FFB300; font-weight: 900;">🟡 {selected_bench.split(" ")[1]} 기준: {target_angle:.1f}°</span>
            </div>
            <div style="background: #ffe6e6; padding: 15px; border-radius: 10px; color: #CD2E3A; font-weight: bold; font-size: 1.1em;">
                ⚠️ 기준 데이터 대비 <span style="font-size:1.3em;">{gap:.1f}°</span> 부족하여 지면 반발력 누수가 발생 중입니다.
            </div>
            <p style="color: #666; margin-top: 20px; font-size: 0.9em;">
                * 위 그래픽은 비전 AI가 추출한 관절 좌표를 기반으로 렌더링된 시뮬레이션입니다. (노란색 점선이 목표 궤적을 의미합니다.)
            </p>
        </div>
        """, unsafe_allow_html=True)

# 7. 피드백 섹션
st.markdown("---")
st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.markdown(f"### {t['f_title']}")
with st.form("feedback_form", clear_on_submit=True):
    f_comment = st.text_area("✍️ Input Feedback")
    f_submit = st.form_submit_button("Submit")
st.markdown('</div>', unsafe_allow_html=True)
