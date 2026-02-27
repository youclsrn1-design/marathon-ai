import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (7대 언어 & 모든 Key 값 일치화하여 KeyError 방지)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "인류의 모든 움직임을 데이터화하는 글로벌 육상 생체역학 파운데이션",
        "s_head": "⚙️ 시스템 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 벤치마크 (국가별)", "s_up": "영상 업로드 (10초)", "s_btn": "🚀 AI 딥 코칭 실행", "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 대조", "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 영어 체육 (Kids)",
        "yt_btn": "📺 추천 교정 훈련 영상 보기",
        "c_sprint_pro": "🎯 <b>[칭찬 및 강점]</b> 폭발적인 가속과 안정적인 상체 기울기가 돋보입니다.<br>⚖️ <b>[장단점 분석]</b> 팔치기 밸런스는 우수하나, 지면 발진 시 무릎 신전력이 약합니다.<br>🚨 <b>[문제 진단]</b> 무릎 신전 <b>{avg_angle}°</b>. <b>{gap:.1f}° 조기 회수</b>로 탄성 에너지가 누수됩니다.<br>💡 <b>[해결 및 훈련법]</b> 뎁스 점프로 발목 강성을 키우고, 전족부 타격 리듬을 익히세요.",
        "c_sprint_kids": "🌟 <b>[Great Job! 최고예요]</b> You run like a rocket! (정말 빨라요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good arms, but look straight! (팔은 좋은데 앞을 봐요!)<br>🔥 <b>[Play: Hot Lava Game 용암 놀이]</b> The ground is lava! Touch it quickly! (바닥이 용암이에요! 앞꿈치로 빨리 터치!)",
        "c_mara_pro": "🎯 <b>[칭찬 및 강점]</b> 흔들림 없는 상체와 일정한 호흡이 매우 뛰어납니다.<br>⚖️ <b>[장단점 분석]</b> 지구력은 좋으나 지면반발력(GRF)의 수직 분산으로 효율이 낮습니다.<br>🚨 <b>[문제 진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 인한 햄스트링 과부하 위험.<br>💡 <b>[해결 및 훈련법]</b> 장요근 스트레칭과 싱글 레그 데드리프트로 골반을 안정시키세요.",
        "c_mara_kids": "🌟 <b>[Great Job! 최고예요]</b> Amazing energy! (에너지가 넘쳐요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good breathing, but don't bounce! (숨쉬기는 좋은데 뛰지 마요!)<br>💧 <b>[Water Cup Game 물컵 놀이]</b> Imagine a water cup on your head! (머리 위에 물컵이 있어요! 닌자처럼 사뿐히!)",
        "c_general_pro": "🎯 <b>[칭찬 및 강점]</b> 기본 자세와 시선 처리가 매우 안정적입니다.<br>⚖️ <b>[장단점 분석]</b> 진입 속도는 좋으나 에너지 전이 단계에서 손실이 발생합니다.<br>🚨 <b>[문제 진단]</b> <b>{avg_angle}°</b> 측정 (<b>{gap:.1f}° 편차</b>). 키네틱 체인의 단절 확인.<br>💡 <b>[해결 및 훈련법]</b> 관절 가동성 훈련과 무게중심(COM) 하강 제어 훈련을 병행하세요.",
        "c_general_kids": "🌟 <b>[Great Job! 최고예요]</b> You look like a champion! (챔피언 같아요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good focus, but use your body! (집중력은 좋은데 온몸을 써봐요!)<br>🚀 <b>[Superhero Move 히어로 놀이]</b> Shrink like a spring, then explode! (용수철처럼 움츠렸다 팡!)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "글로벌 표준 데이터를 스마트 안경(AR)에 투사하는 플랫폼입니다.", "f_title": "🧪 AI 연구소", "f_desc": "여러분의 의견을 남겨주세요."
    },
    "🇺🇸 English": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Global Biomechanics Foundation Digitizing Human Movement",
        "s_head": "⚙️ Settings", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Coaching", "r_title": "🔬 AI Biomechanics Report", "img_title": "📸 Vision AI Tracking", "tab_pro": "🎓 Pro Biomechanics", "tab_kids": "🎈 Easy English Kids",
        "yt_btn": "📺 Watch Recommended Drill Video",
        "c_sprint_pro": "🎯 <b>[Praise]</b> Great acceleration and posture.<br>⚖️ <b>[Pros & Cons]</b> Good arms, weak ground force.<br>🚨 <b>[Diagnosis]</b> Knee ext <b>{avg_angle}°</b>. <b>{gap:.1f}° early recovery</b> leak.<br>💡 <b>[Solution]</b> Depth jumps for ankle stiffness and forefoot rhythm.",
        "c_sprint_kids": "🌟 <b>[Great Job!]</b> You run like a rocket!<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less!<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly with your toes!",
        "c_mara_pro": "🎯 <b>[Praise]</b> Stable torso and breathing.<br>⚖️ <b>[Pros & Cons]</b> Great endurance, poor efficiency.<br>🚨 <b>[Diagnosis]</b> <b>{gap:.1f}° deviation</b>. Vertical energy dispersion.<br>💡 <b>[Solution]</b> Iliopsoas stretch and single-leg deadlifts.",
        "c_mara_kids": "🌟 <b>[Great Job!]</b> Amazing energy!<br>🔍 <b>[Pros & Cons]</b> Good breathing, don't bounce!<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! Glide like a ninja!",
        "c_general_pro": "🎯 <b>[Praise]</b> Elite-level basic posture.<br>⚖️ <b>[Pros & Cons]</b> Good speed, weak energy transfer.<br>🚨 <b>[Diagnosis]</b> <b>{avg_angle}°</b> (<b>{gap:.1f}° deviation</b>).<br>💡 <b>[Solution]</b> Mobility drills and COM drop control.",
        "c_general_kids": "🌟 <b>[Great Job!]</b> You look like a champion!<br>🔍 <b>[Pros & Cons]</b> Good focus, use your whole body!<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode!",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Projecting global athletics data into AR glasses.", "f_title": "🧪 AI Lab", "f_desc": "Leave your feedback."
    }
    # (일어, 중국어, 스페인어, 힌디어, 프랑스어 딕셔너리도 동일한 Key 구조로 포함됨 - 공간상 요약)
}

# 3. 🏟️ 육상 종목 & 유튜브 링크 매핑 DB
categories = {
    "Track (트랙/달리기)": {
        "metrics": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 밸런스', '상하체 동기화'],
        "sports": ["100m 단거리 (Sprint)", "400m 스프린트", "마라톤 (Marathon)", "100m/110m 허들", "경보 (Race Walking)"]
    },
    "Jump (도약/뛰기)": {
        "metrics": ['도약 무릎각', '무게중심 강하', '진입 속도', '체공 시간', '착지 안정성'],
        "sports": ["멀리뛰기 (Long Jump)", "세단뛰기 (Triple Jump)", "높이뛰기 (High Jump)", "장대높이뛰기 (Pole Vault)"]
    },
    "Throw (투척/던지기)": {
        "metrics": ['릴리스 각도', '투척 속도', '앞발 블록킹', '몸통 비틀림', '어깨 회전축'],
        "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]
    }
}

# [핵심] 종목별 추천 교정 훈련 유튜브 링크
yt_links = {
    "Sprint": "https://www.youtube.com/results?search_query=sprinter+leg+recovery+drills",
    "Distance": "https://www.youtube.com/results?search_query=marathon+running+form+correction",
    "Jump": "https://www.youtube.com/results?search_query=long+jump+takeoff+technique",
    "Throw": "https://www.youtube.com/results?search_query=javelin+throw+blocking+drill",
    "Walk": "https://www.youtube.com/results?search_query=race+walking+technique+drills"
}

benchmark_db = {
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇮🇳 India": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}}
}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .hero-section { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 50px 20px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .hero-title { color: #64FFDA; font-size: 3.5em; font-weight: 900; letter-spacing: 1px; margin-bottom: 10px; }
    .hero-sub { color: #CCD6F6; font-size: 1.2em; font-weight: 400; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    
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

# 🚀 Hero Section
st.markdown(f"""<div class="hero-section"><h1 class="hero-title">{t['title']}</h1><p class="hero-sub">{t['sub']}</p></div>""", unsafe_allow_html=True)

# 6. 메인 분석
if video_file and analyze_btn:
    with st.spinner('Fixing Bugs & Adding YouTube Links...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        if b_group_name == "Sprint": avg_angle = 158.5
        elif b_group_name == "Distance": avg_angle = 155.9
        elif b_group_name == "Walk": avg_angle = 172.0
        elif b_group_name == "Jump": avg_angle = 162.5
        elif b_group_name == "Throw": avg_angle = 158.0
        target_angle = b_data['angle']; gap = target_angle - avg_angle
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
        fig_radar = go.Figure(); fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#D93025'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name="Target", line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.3])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin: 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8)))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8)))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=500, showlegend=False)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        if b_group_name == "Sprint":
            with tab_pro: 
                st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
                st.link_button(t['yt_btn'], yt_links["Sprint"])
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: 
                st.markdown(t['c_mara_pro'].format(gap=gap), unsafe_allow_html=True)
                st.link_button(t['yt_btn'], yt_links["Distance"])
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        else:
            with tab_pro: 
                st.markdown(t['c_general_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
                st.link_button(t['yt_btn'], yt_links[b_group_name])
            with tab_kids: st.markdown(t['c_general_kids'], unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""<div style="background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 40px; border-radius: 12px;"><h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3><p>{t['vision_desc']}</p></div>""", unsafe_allow_html=True)

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
            req = urllib.request.Request(url, data=encoded_data); urllib.request.urlopen(req)
            st.balloons(); st.success("Success!")
        except: st.error("Error")
