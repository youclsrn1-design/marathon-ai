import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (5대 언어)
ui_langs = {
    "🇰🇷 한국어": {"title": "ATHLETICS AI FOUNDATION", "sub": "글로벌 육상 전 종목 생체역학 교육 시스템", "toss": "Toss ID: ATHLETICS AI", "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 비교 벤치마크 (국가별)", "s_up": "측면 영상 파일 선택 (10초 이내)", "s_btn": "🚀 AI 정밀 분석 및 지도법 생성", "r_title": "🔬 생체역학 진단 및 교육 리포트", "img_title": "📸 비전 AI 관절 추출 및 종목별 궤적 대조", "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 훈련 지도법", "vision_title": "🛰️ Future Mission: 인류의 모든 움직임을 데이터화하다", "vision_desc": "마라톤, 100m, 창던지기 등 육상 15개 전 종목의 국가별 생체역학 DB를 스마트 안경(AR)에 실시간 투사하는 파운데이션 모델입니다.", "f_title": "🧪 ATHLETICS 연구소", "f_desc": "당신의 의견이 더 똑똑한 AI 코치를 만듭니다.", "f_success": "✅ 의견이 AI 연구소로 성공적으로 전송되었습니다!",
        "c_sprint_pro": "<b>[단거리 역학]</b> 도약 시 무릎 신전이 {avg_angle}°에 그쳐 {gap:.1f}° 조기 회수 관찰. SSC 에너지 누수.<br><b>[훈련]</b> 뎁스 점프로 발목 강성 강화", "c_sprint_kids": "<b>[용암 밟기 놀이]</b> 바닥이 뜨거운 용암이에요! 앞꿈치로만 잽싸게 땅을 치고 로켓처럼 튀어 나가세요!",
        "c_mara_pro": "<b>[마라톤 효율]</b> 불완전 신전으로 {gap:.1f}° 편차. GRF 수직 분산.<br><b>[훈련]</b> 장요근 동적 스트레칭 및 코어 안정화", "c_mara_kids": "<b>[머리 위 물컵 지키기]</b> 쿵쾅거리면 물이 쏟아져요! 위아래로 흔들리지 말고 닌자처럼 사뿐사뿐 달리세요.",
        "c_jump_pro": "<b>[도약 역학]</b> 마지막 걸음에서 무게중심 하강비 부족.<br><b>[훈련]</b> 힌지 제어 및 상향 스윙 매칭", "c_jump_kids": "<b>[마법의 징검다리]</b> 뛰기 직전 무릎을 살짝 더 굽히고, 마지막에 '쾅!' 밟으며 만세! 하고 솟아오르세요.",
        "c_throw_pro": "<b>[투척 역학]</b> 리드 레그 블록킹 붕괴로 키네틱 체인 단절.<br><b>[훈련]</b> 브레이싱 훈련 및 흉추 가동성 확장", "c_throw_kids": "<b>[인간 투석기 놀이]</b> 던지기 직전 앞발을 딛으며 '얼음!' 멈추고, 상체만 채찍처럼 휙! 던지세요.", "c_walk_pro": "<b>[경보 판정]</b> Straight Leg Rule 위반 감지. {gap:.1f}° 편차로 파울 위험.<br><b>[훈련]</b> 착지 시 무릎 관절 100% 락킹 훈련", "c_walk_kids": "<b>[모델 걷기 놀이]</b> 경보에서는 무릎이 굽혀지면 반칙이에요! 앞다리를 쭉쭉 펴고 골반을 흔들며 걸어봐요!"
    },
    "🇺🇸 English": {"title": "ATHLETICS AI FOUNDATION", "sub": "Global Track & Field Biomechanics System", "toss": "Powered by ATHLETICS AI", "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark (By Country)", "s_up": "Select Video (Max 10s)", "s_btn": "🚀 Run AI Analysis", "r_title": "🔬 Biometric Diagnostic Report", "img_title": "📸 Vision AI Skeletal Tracking", "tab_pro": "🎓 Pro Biomechanics", "tab_kids": "🎈 Kids Drill", "vision_title": "🛰️ Future Mission: Digitizing Human Movement", "vision_desc": "A Foundation Model projecting country-specific biomechanics for 15 events into AR Smart Glasses.", "f_title": "🧪 ATHLETICS AI Lab", "f_desc": "Your feedback builds a smarter AI.", "f_success": "✅ Feedback submitted successfully!",
        "c_sprint_pro": "<b>[Sprint]</b> Knee ext at {avg_angle}°. {gap:.1f}° early recovery. SSC leak.<br><b>[Drill]</b> Depth jumps for ankle stiffness.", "c_sprint_kids": "<b>[Hot Lava]</b> The ground is hot lava! Touch quickly with toes and blast off!",
        "c_mara_pro": "<b>[Marathon]</b> {gap:.1f}° deviation. Vertical GRF dispersion.<br><b>[Drill]</b> Iliopsoas stretch & Single-leg deadlifts.", "c_mara_kids": "<b>[Water Cup]</b> Imagine a water cup on your head! Don't bounce, glide like a ninja.",
        "c_jump_pro": "<b>[Jump]</b> Insufficient COM drop in penultimate step.<br><b>[Drill]</b> Hinge control and upward arm drive.", "c_jump_kids": "<b>[Frog Jump]</b> Bend knees on the last step, stomp, and fly like Superman!",
        "c_throw_pro": "<b>[Throw]</b> Weak blocking breaks kinetic chain.<br><b>[Drill]</b> Bracing drills and thoracic mobility.", "c_throw_kids": "<b>[Catapult]</b> Plant front foot, yell 'Freeze!', and whip your upper body!", "c_walk_pro": "<b>[Race Walk]</b> Straight Leg Rule violation. {gap:.1f}° bent knee.<br><b>[Drill]</b> 100% knee locking on contact.", "c_walk_kids": "<b>[Model Walk]</b> Keep your front leg completely straight and swing your hips!"
    }
}

# 3. 🏟️ 육상 전 종목 카테고리
categories = {
    "Track (트랙/달리기)": {
        "metrics": ['무릎 신전(Knee Ext)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 밸런스(Pelvic)', '상하체 동기화(Arm Sync)'],
        "sports": ["100m 단거리 (Sprint)", "400m 스프린트", "마라톤 (Marathon)", "100m/110m 허들", "경보 (Race Walking)"]
    },
    "Jump (도약/뛰기)": {
        "metrics": ['도약 무릎각(Take-off)', '무게중심 강하(COM Drop)', '진입 속도(Approach)', '체공 시간(Flight)', '착지 안정성(Landing)'],
        "sports": ["멀리뛰기 (Long Jump)", "세단뛰기 (Triple Jump)", "높이뛰기 (High Jump)", "장대높이뛰기 (Pole Vault)"]
    },
    "Throw (투척/던지기)": {
        "metrics": ['릴리스 팔각도(Release)', '투척 속도(Velocity)', '앞발 블록킹(Blocking)', '몸통 비틀림(Trunk)', '어깨 회전축(Shoulder)'],
        "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]
    }
}

# 🚀 [핵심] 종목별 최강국 벤치마크 DB 분리 (구글 AR 안경 연동용)
benchmark_db = {
    "Sprint": {
        "🌍 World Record (세계 신기록)": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"},
        "🇯🇲 Jamaica Elite (자메이카)": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"},
        "🇺🇸 US Elite (미국)": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"},
        "🇰🇷 Korea Elite (한국)": {"angle": 167.5, "radar": [88, 90, 82, 88, 90], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반)": {"angle": 150.0, "radar": [60, 50, 65, 55, 60], "color": "#888888"}
    },
    "Distance": {
        "🌍 World Record (세계 신기록)": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"},
        "🇰🇪 Kenya Elite (케냐)": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"},
        "🇯🇵 Japan Elite (일본)": {"angle": 163.5, "radar": [87, 89, 82, 87, 91], "color": "#BC002D"},
        "🇰🇷 Korea Elite (한국)": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반)": {"angle": 155.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
    },
    "Walk": {
        "🌍 World Record (세계 신기록)": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"},
        "🇨🇳 China Elite (중국)": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"},
        "🇪🇸 Spain Elite (스페인)": {"angle": 178.8, "radar": [96, 92, 95, 96, 94], "color": "#F1BF00"},
        "🇰🇷 Korea Elite (한국)": {"angle": 178.5, "radar": [95, 90, 92, 94, 90], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반)": {"angle": 165.0, "radar": [40, 75, 85, 50, 60], "color": "#888888"}
    },
    "Jump": {
        "🌍 World Record (세계 신기록)": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"},
        "🇨🇺 Cuba Elite (쿠바)": {"angle": 177.5, "radar": [96, 94, 98, 93, 94], "color": "#CB1515"},
        "🇺🇸 US Elite (미국)": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"},
        "🇰🇷 Korea Elite (한국)": {"angle": 170.0, "radar": [85, 88, 82, 85, 88], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반)": {"angle": 155.0, "radar": [50, 60, 55, 50, 65], "color": "#888888"}
    },
    "Throw": {
        "🌍 World Record (세계 신기록)": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"},
        "🇩🇪 Germany Elite (독일)": {"angle": 174.5, "radar": [96, 98, 97, 95, 96], "color": "#FFCE00"},
        "🇨🇿 Czech Elite (체코)": {"angle": 173.0, "radar": [95, 97, 95, 94, 95], "color": "#11457E"},
        "🇰🇷 Korea Elite (한국)": {"angle": 168.0, "radar": [85, 88, 86, 85, 87], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반)": {"angle": 150.0, "radar": [55, 60, 50, 55, 60], "color": "#888888"}
    }
}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .header-panel { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 35px 30px; border-radius: 16px; color: white; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-left: 6px solid #64FFDA; padding: 25px; border-radius: 0 12px 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; border-top: 1px solid #E8EAED; border-right: 1px solid #E8EAED; border-bottom: 1px solid #E8EAED; }
    .vision-card { background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 구성 (동적 DB 연동)
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", ["🇰🇷 한국어", "🇺🇸 English"])
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    
    # 선택된 종목에 따라 국가별 DB 매칭
    if "Jump" in selected_cat: b_group_name = "Jump"
    elif "Throw" in selected_cat: b_group_name = "Throw"
    else:
        if "경보" in selected_sport or "Walk" in selected_sport: b_group_name = "Walk"
        elif "마라톤" in selected_sport or "Marathon" in selected_sport: b_group_name = "Distance"
        else: b_group_name = "Sprint"
        
    b_group = benchmark_db[b_group_name]
    
    selected_bench = st.selectbox(t['s_data'], list(b_group.keys()))
    b_data = b_group[selected_bench]
    
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov', 'avi'])
    analyze_btn = st.button(t['s_btn'], use_container_width=True, type="primary")

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.4em; color:#64FFDA;'>🌍 {t['title']}</h1>
        <p style='margin:5px 0 0 0; color:#CCD6F6;'>{t['sub']}</p></div>
        <div><span style="background: rgba(100,255,218,0.1); color: #64FFDA; padding: 10px 25px; border-radius: 30px; font-weight: 800; border: 1px solid rgba(100,255,218,0.3);">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 딥러닝 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('Accessing Global Database...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        
        # 종목별 내 각도(Mock Data) 동적 적용
        if b_group_name == "Sprint": avg_angle = 158.5
        elif b_group_name == "Distance": avg_angle = 155.9
        elif b_group_name == "Walk": avg_angle = 172.0
        elif b_group_name == "Jump": avg_angle = 162.5
        elif b_group_name == "Throw": avg_angle = 158.0
        
        target_angle = b_data['angle']; gap = target_angle - avg_angle
        bench_name = selected_bench.split(" ")[0]
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0A192F"}, 'steps': [{'range': [0, 70], 'color': "#FCE8E6"}, {'range': [85, 100], 'color': "#E6F4EA"}], 'threshold': {'line': {'color': "#64FFDA", 'width': 4}, 'value': 95}}))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#D93025'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin: 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), name='Axis'))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8), name=f'My ({avg_angle}°)'))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'Standard ({target_angle}°)'))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=480, showlegend=True)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        
        if b_group_name == "Sprint":
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: st.markdown(t['c_mara_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        elif b_group_name == "Walk":
            with tab_pro: st.markdown(t['c_walk_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_walk_kids'], unsafe_allow_html=True)
        elif b_group_name == "Jump":
            with tab_pro: st.markdown(t['c_jump_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_jump_kids'], unsafe_allow_html=True)
        elif b_group_name == "Throw":
            with tab_pro: st.markdown(t['c_throw_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_throw_kids'], unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown(f"""<div class="vision-card"><h3 style="color: #1A73E8;">{t['vision_title']}</h3><p>{t['vision_desc']}</p></div>""", unsafe_allow_html=True)

# 8. 구글 엑셀 연동
st.markdown("---")
with st.form(key='athletics_ai_form', clear_on_submit=True):
    user_comment = st.text_area(t['f_title'], placeholder=t['f_desc'])
    submit_button = st.form_submit_button(label="Submit", type="primary")
    if submit_button and user_comment:
        try:
            url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
            data = {"entry.503694872": user_comment}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data)
            urllib.request.urlopen(req)
            st.balloons(); st.success(t['f_success'])
        except: st.error("Error")
