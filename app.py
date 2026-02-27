import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (육상 통합 파운데이션 비전으로 업그레이드)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "글로벌 육상 전 종목 생체역학 통합 분석 시스템", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", 
        "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목",
        "s_data": "📊 비교 벤치마크", "s_up": "측면 영상 파일 선택 (10초 이내)", 
        "s_btn": "🚀 파운데이션 AI 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "img_title": "📸 비전 AI 관절 추출 및 종목별 궤적 대조",
        "img_desc": "표준화된 관절 좌표를 기반으로 트랙, 도약, 투척 등 육상 전 종목의 핵심 역학 궤적을 분석합니다.",
        "vision_title": "🛰️ Future Mission: 인류의 모든 움직임을 데이터화하다",
        "vision_desc": "본 시스템은 마라톤, 100m, 창던지기, 높이뛰기 등 육상(Track and Field) 15개 전 종목의 생체역학을 하나의 AI로 통합한 '파운데이션 모델'입니다. 이를 기반으로 전 세계 모든 스포츠의 기준을 세웁니다.",
        "f_title": "🧪 ATHLETICS AI 연구소", "f_desc": "당신의 폼이 세계의 표준이 됩니다. 딥러닝 분석 결과에 대한 자유로운 의견을 남겨주세요.",
        "f_success": "✅ 귀하의 소중한 의견이 AI 연구소(Google Sheets)로 성공적으로 실시간 전송되었습니다!"
    },
    "🇺🇸 English": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Global Track & Field Biomechanics System", "toss": "Powered by ATHLETICS AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", 
        "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event",
        "s_data": "📊 Benchmark Target", "s_up": "Select Video File (Side-view)", 
        "s_btn": "🚀 Run Foundation AI", "r_title": "🔬 Biometric Diagnostic Report",
        "img_title": "📸 Vision AI Skeletal Tracking",
        "img_desc": "Analyzes core kinetic trajectories across all track, jump, and throw events.",
        "vision_title": "🛰️ Future Mission: Digitizing Human Movement",
        "vision_desc": "This is a Foundation Model integrating biomechanics for all 15 Track & Field events. We set the standard for all sports worldwide.",
        "f_title": "🧪 ATHLETICS AI Lab", "f_desc": "Your form becomes the global standard. Please leave your feedback.",
        "f_success": "✅ Your feedback has been successfully submitted to our Google Sheets database!"
    }
}

# 3. 🏟️ 육상 전 종목 카테고리 및 동적 평가지표 설계
categories = {
    "트랙 (Track: 달리기/허들)": {
        "metrics": ['무릎 신전(Knee Ext)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 밸런스(Pelvic)', '상하체 동기화(Arm Sync)'],
        "sports": ["100m 단거리", "400m 스프린트", "800m 중거리", "1500m 중거리", "5000m 장거리", "10000m 장거리", "마라톤 (Marathon)", "100m/110m 허들", "400m 허들", "경보 (Race Walking)"]
    },
    "도약 (Jump: 뛰기)": {
        "metrics": ['발구름 각도(Take-off)', '무게중심 상승(COM)', '진입 속도(Approach)', '체공 시간(Flight)', '착지 안정성(Landing)'],
        "sports": ["멀리뛰기 (Long Jump)", "세단뛰기 (Triple Jump)", "높이뛰기 (High Jump)", "장대높이뛰기 (Pole Vault)"]
    },
    "투척 (Throw: 던지기)": {
        "metrics": ['릴리스 각도(Release)', '투척 속도(Velocity)', '블록킹(Blocking)', '몸통 비틀림(Trunk)', '어깨 회전축(Shoulder)'],
        "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]
    }
}

# 벤치마크 (시연용 공통 데이터 구조 적용)
benchmarks = {
    "🌍 World Record (세계 신기록)": {"angle": 175.5, "radar": [99, 98, 97, 99, 98], "color": "#000000"},
    "🥇 Olympic Gold (올림픽 금메달)": {"angle": 172.0, "radar": [96, 95, 96, 95, 97], "color": "#F1BF00"},
    "🇰🇷 Korea Elite (국가대표)": {"angle": 165.5, "radar": [88, 90, 85, 88, 90], "color": "#CD2E3A"},
    "🌐 Amateur (일반인 평균)": {"angle": 150.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .header-panel { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 35px 30px; border-radius: 16px; color: white; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-left: 6px solid #64FFDA; padding: 25px; border-radius: 0 12px 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; border-top: 1px solid #E8EAED; border-right: 1px solid #E8EAED; border-bottom: 1px solid #E8EAED; }
    .highlight-text { color: #D93025; font-weight: 800; }
    .vision-card { background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px; margin-top: 40px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(26,115,232,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 구성 (2단계 선택 로직)
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    selected_bench = st.selectbox(t['s_data'], list(benchmarks.keys()))
    b_data = benchmarks[selected_bench]
    
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov', 'avi'])
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button(t['s_btn'], use_container_width=True, type="primary")

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.4em; letter-spacing: -1px; color:#64FFDA;'>🌍 {t['title']}</h1>
        <p style='margin:5px 0 0 0; color:#CCD6F6; font-size: 1.1em;'>{t['sub']}</p></div>
        <div><span style="background: rgba(100,255,218,0.1); color: #64FFDA; padding: 10px 25px; border-radius: 30px; font-weight: 800; border: 1px solid rgba(100,255,218,0.3);">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 딥러닝 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('Foundation AI Engine Processing...'):
        score = 78 
        my_stats = [75, 68, 85, 70, 65] 
        avg_angle = 155.9 
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        bench_name = selected_bench.split(" ")[0]
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3 style='color: #202124;'>{t['r_title']} ({selected_sport})</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=score, title={'text': "AI 역학 일치도 (Score)", 'font': {'size': 18, 'color': '#5F6368'}},
            domain={'x': [0, 1], 'y': [0, 1]}, 
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#0A192F"},
                'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "#E8EAED",
                'steps': [{'range': [0, 70], 'color': "#FCE8E6"}, {'range': [85, 100], 'color': "#E6F4EA"}],
                'threshold': {'line': {'color': "#64FFDA", 'width': 4}, 'value': 95}
            }))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#202124", 'family': "Pretendard"})
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#D93025', fillcolor='rgba(217, 48, 37, 0.2)'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E8EAED', linecolor='#E8EAED')), 
            showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#5F6368", 'family': "Pretendard", 'size': 11}
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.markdown(f"""
            <div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;">
                <h5 style="color: #202124; margin-top: 0; margin-bottom: 5px;">{t['img_title']}</h5>
            </div>
        """, unsafe_allow_html=True)
        
        x_my_ankle = -np.sin(np.radians(180 - avg_angle))
        y_my_ankle = -np.cos(np.radians(180 - avg_angle))
        x_target_ankle = -np.sin(np.radians(180 - target_angle))
        y_target_ankle = -np.cos(np.radians(180 - target_angle))

        fig_overlay = go.Figure()
        fig_overlay.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), marker=dict(size=14, color='white'), name='고정축'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_my_ankle], y=[0, y_my_ankle], mode='lines+markers', line=dict(color='#D93025', width=8), marker=dict(size=14, color='#D93025'), name=f'내 궤적 ({avg_angle}°)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_target_ankle], y=[0, y_target_ankle], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'파운데이션 표준 ({target_angle}°)'))

        fig_overlay.update_layout(
            plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white', family='Pretendard'),
            xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]),
            margin=dict(l=20, r=20, t=20, b=20), height=400, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_easy = st.tabs(["🎓 파운데이션 역학 리포트", "🎈 AI 핵심 코칭"])
        
        # 💡 종목 카테고리에 따른 소름 돋는 동적 피드백
        if "Track" in selected_cat:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">🏃‍♂️ 트랙(Track) 하체 발진 메커니즘 분석</h4>
                <p style="font-size: 0.95em; color: #5F6368; line-height: 1.6;">
                    육상 트랙 종목의 핵심인 도약(Push-off) 무릎 신전 각도가 <span class="highlight-text">{avg_angle}°</span>로 산출되었습니다. 
                    세계 기준({target_angle}°) 대비 <span class="highlight-text">{gap:.1f}° 편차</span>를 보이며, 이는 하퇴 삼두근의 불완전 수축으로 인한 지면반발력(GRF) 누수를 의미합니다.
                </p>
                """)
            with tab_easy:
                st.markdown("<b>'땅을 끝까지 밀어내세요!'</b><br>세계적인 선수들처럼 다리를 쫙 펴서 지면을 끝까지 차고 나가야 에너지를 아낄 수 있어요.")
        elif "Jump" in selected_cat:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">🦘 도약(Jump) 발구름(Take-off) 메커니즘 분석</h4>
                <p style="font-size: 0.95em; color: #5F6368; line-height: 1.6;">
                    도약 종목의 생명인 발구름판 진입 및 도약 각도가 <span class="highlight-text">{avg_angle}°</span>로 측정되었습니다. 
                    세계 기준 대비 <span class="highlight-text">{gap:.1f}° 누수</span>가 발생하여, 진입 속도(Approach Speed)가 무게중심(COM)의 수직 상승 에너지로 100% 전환되지 못하고 있습니다.
                </p>
                """)
            with tab_easy:
                st.markdown("<b>'발구름판을 강하게 찍고 솟아오르세요!'</b><br>달려온 속도를 그대로 위로 튕겨내려면 마지막 발구름 각도가 완벽해야 합니다.")
        else: # Throw
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">☄️ 투척(Throw) 릴리스 및 블록킹 분석</h4>
                <p style="font-size: 0.95em; color: #5F6368; line-height: 1.6;">
                    투구구간 손에서 기구가 떠나는 릴리스(Release) 궤적 각도가 <span class="highlight-text">{avg_angle}°</span>로 분석되었습니다. 
                    이상적인 투사각({target_angle}°) 대비 <span class="highlight-text">{gap:.1f}° 오차</span>가 있으며, 하체의 브레이킹(Blocking) 동작이 약해 상체 회전축으로 힘이 완전히 전달되지 못했습니다.
                </p>
                """)
            with tab_easy:
                st.markdown("<b>'하체로 버티고 상체로 채찍처럼 던지세요!'</b><br>앞다리가 벽처럼 튼튼하게 버텨주어야(블록킹), 그 힘이 어깨를 타고 던지는 각도로 100% 전달됩니다.")
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 🛰️ 파운데이션 비전 섹션
st.markdown(f"""
    <div class="vision-card">
        <h3 style="color: #1A73E8; margin-top: 0; display: flex; align-items: center; gap: 10px;">{t['vision_title']}</h3>
        <p style="font-size: 1.1em; color: #3C4043; line-height: 1.6; margin-bottom: 20px;">{t['vision_desc']}</p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <span style="background: #E8F0FE; color: #1A73E8; padding: 6px 16px; border-radius: 20px; font-weight: 800; border: 1px solid #D2E3FC;">#Track_And_Field_Foundation_AI</span>
            <span style="background: #E8F0FE; color: #1A73E8; padding: 6px 16px; border-radius: 20px; font-weight: 800; border: 1px solid #D2E3FC;">#All_Sports_Standard</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 8. 🧪 구글 엑셀 실시간 연동
st.markdown("---")
st.markdown('<div class="data-card" style="margin-bottom: 50px;">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #202124;'>{t['f_title']}</h3>", unsafe_allow_html=True)
st.write(f"<span style='color: #5F6368;'>{t['f_desc']}</span>", unsafe_allow_html=True)

with st.form(key='marathon_ai_lab_form', clear_on_submit=True):
    user_comment = st.text_area("연구소로 데이터 전송 (Data Submission)", placeholder="예: '창던지기와 멀리뛰기까지 분석되다니 정말 놀랍습니다!'")
    submit_button = st.form_submit_button(label="의견 전송 및 파운데이션 구축 참여 (Submit)", type="primary")

    if submit_button:
        if user_comment:
            try:
                url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
                data = {"entry.503694872": user_comment}
                encoded_data = urllib.parse.urlencode(data).encode("utf-8")
                req = urllib.request.Request(url, data=encoded_data)
                urllib.request.urlopen(req)
                st.balloons()
                st.success(t['f_success'])
            except Exception as e:
                st.error("⚠️ 데이터 전송 중 오류가 발생했습니다.")
        else:
            st.warning("의견을 먼저 입력해 주세요.")
st.markdown('</div>', unsafe_allow_html=True)
