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
        "img_desc": "가장 추진력이 필요한 '도약(Push-off)' 프레임을 자동 캡처하여, 사용자의 무릎 각도와 선택한 국가 대표의 <b><span style='color:#FFB300;'>이상적인 기준선(노란선)</span></b>을 대조합니다.",
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
        "img_desc": "Automatically captures the 'Push-off' frame to overlay your knee angle against the <b><span style='color:#FFB300;'>Ideal Guideline (Yellow Line)</span></b> of the selected benchmark.",
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
    .overlay-box { background: #fdfdfd; border: 2px dashed #ccc; border-radius: 15px; padding: 40px 20px; text-align: center; margin-top: 20px; position: relative; }
    .asian-focus { background-color: #f8f9fa; border-left: 4px solid #BC002D; padding: 15px; margin-top: 15px; font-size: 0.95em; color: black; }
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
        u_angle = np.random.normal(158.2, 3.5, 100)
        avg_angle = np.mean(u_angle)
        gap = b_data['angle'] - avg_angle
        
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

    # 📸 새로운 비전 이미지 오버레이 섹션 (AR 대체)
    st.markdown(f"""
        <div class="data-card" style="margin-top: 20px; border-top: 5px solid #FFB300;">
            <h4 style="color: #002D62; margin-top: 0;">{t['img_title']}</h4>
            <p style="color: #555;">{t['img_desc']}</p>
            
            <div class="overlay-box">
                <div style="display: inline-block; text-align: left; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); width: 80%; max-width: 500px;">
                    <h5 style="margin-top:0; color: #333; text-align: center;">🏃‍♂️ Frame #045 (Push-off Phase)</h5>
                    <div style="font-size: 1.2em; margin: 15px 0;">
                        <span style="color: #CD2E3A; font-weight: 900;">🔴 사용자 무릎 신전: {avg_angle:.1f}°</span><br>
                        <span style="color: #FFB300; font-weight: 900;">🟡 {selected_bench.split(" ")[1]} 기준선: {b_data['angle']}°</span>
                    </div>
                    <div style="background: #ffe6e6; padding: 10px; border-radius: 8px; color: #CD2E3A; font-weight: bold; text-align: center;">
                        ⚠️ 분석 결과: 기준 데이터 대비 {gap:.1f}° 부족합니다.
                    </div>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
                    <p style="font-size: 0.85em; color: #888; text-align: center; margin: 0;">
                        ※ 실제 서비스 앱 배포 시, 이 공간에 사용자의 러닝 프레임 이미지 위에 두 개의 각도 선(빨간선, 노란선)이 교차하는 컴퓨터 비전(CV) 오버레이 화면이 표출됩니다.
                    </p>
                </div>
            </div>
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
