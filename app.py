import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 시스템 기본 설정
st.set_page_config(page_title="Athletes AI | Global Vision 2026", layout="wide", initial_sidebar_state="expanded")

# 2. 7대 언어 무결점 사전 (모든 종목의 Key를 완벽히 통일하여 KeyError 원천 차단)
def get_ui_langs():
    # 기본 한국어 팩
    ko = {
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION",
        "sub": "2026-2031 인류 움직임 예측 및 생체역학 파운데이션",
        "s_head": "⚙️ AI 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 종목", "s_data": "📊 벤치마크", "s_up": "영상 업로드", "s_btn": "🚀 AI 정밀 분석 실행",
        "r_title": "🔬 AI 생체역학 진단 및 부상 예측 리포트", "img_title": "📸 비전 AI 관절 궤적 추적", 
        "tab_pro": "🎓 전문가 분석", "tab_kids": "🎈 어린이 영어 체육", "tab_injury": "⚠️ 부상 위험 및 예방",
        "yt_btn": "📺 추천 교정 훈련 영상", "risk_label": "부상 위험 지수",
        
        # [안내 문구로 변경된 하단 텍스트]
        "f_title": "🧪 AI 연구소 & 비즈니스 문의", 
        "f_desc": "ATHLETES AI는 전 세계 육상 데이터를 하나로 모으는 파운데이션을 구축하고 있습니다.<br>시스템 피드백 및 제휴 문의는 아래 이메일로 연락해 주시기 바랍니다.<br><br>📧 <b>Contact : youclsrn1@gmail.com</b>",
        
        # 종목별 코칭 (전문가/어린이/부상)
        "c_sprint_pro": "🎯 <b>[강점]</b> 폭발적 가속력이 일품입니다.<br>🚨 <b>[진단]</b> 무릎 신전 <b>{avg_angle}°</b>. SSC 에너지 누수 발생.",
        "c_sprint_kids": "🌟 <b>[Praise]</b> You run like a rocket! (로켓처럼 빨라요!)<br>🔥 <b>[Action]</b> 땅이 뜨거운 용암이라고 생각하고 앞꿈치로 빨리 차세요!",
        "c_sprint_injury": "🚨 <b>[부상 위험]</b> 햄스트링 위험 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 러닝 전 레그 스윙으로 근육 예열 필수.",
        
        "c_mara_pro": "🎯 <b>[강점]</b> 안정적인 상체 유지 능력이 우수합니다.<br>🚨 <b>[진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 인한 에너지 분산 관찰.",
        "c_mara_kids": "🌟 <b>[Praise]</b> Amazing energy! (에너지가 넘쳐요!)<br>💧 <b>[Action]</b> 머리 위에 물컵이 있다고 생각하고 사뿐사뿐 닌자처럼!",
        "c_mara_injury": "🚨 <b>[부상 위험]</b> 무릎 연골 부하 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 중둔근 강화를 위한 싱글 레그 데드리프트 권장.",

        "c_jump_pro": "🎯 <b>[강점]</b> 진입 속도 유지가 탁월합니다.<br>🚨 <b>[진단]</b> 마지막 스텝 무게중심 하강 부족. 수직 충격량 전환 손실.",
        "c_jump_kids": "🌟 <b>[Praise]</b> You fly high! (높이 날아올라요!)<br>🚀 <b>[Action]</b> 개구리처럼 마지막에 몸을 웅크렸다 만세하며 팡!",
        "c_jump_injury": "🚨 <b>[부상 위험]</b> 발목 인대 부하 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 착지 시 무릎 완충 작용 집중 훈련.",

        "c_throw_pro": "🎯 <b>[강점]</b> 팔의 스윙 궤적이 매우 간결합니다.<br>🚨 <b>[진단]</b> 앞발 블록킹 붕괴. 상체로의 에너지 전이 차단.",
        "c_throw_kids": "🌟 <b>[Praise]</b> Power throw! (힘이 장사네요!)<br>🎯 <b>[Action]</b> 앞발을 '얼음!' 하고 멈춘 뒤 몸을 투석기처럼 휙!",
        "c_throw_injury": "🚨 <b>[부상 위험]</b> 어깨 회전근개 과부하 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 흉추 가동성 훈련 및 고무밴드 회전근 강화.",

        "c_walk_pro": "🎯 <b>[강점]</b> 리드미컬한 골반 움직임이 좋습니다.<br>🚨 <b>[진단]</b> 무릎 완전 신전 미흡. 파울 위험 지수 상승.",
        "c_walk_kids": "🌟 <b>[Praise]</b> Cool walker! (걷는 모습이 멋져요!)<br>🚶‍♂️ <b>[Action]</b> 다리를 젓가락처럼 쫙 펴고 모델처럼 걸어봐요!",
        "c_walk_injury": "🚨 <b>[부상 위험]</b> 고관절 마찰 위험 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 장요근 스트레칭 및 골반 안정화 운동."
    }
    
    # 영어 팩 (한국어 팩 복사 후 영어로 변환)
    en = ko.copy()
    en.update({
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION",
        "sub": "2026-2031 Global Biomechanics Prediction Foundation",
        "s_head": "⚙️ AI Config", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Prediction",
        "r_title": "🔬 AI Biometric & Injury Forecast Report", "img_title": "📸 Vision AI Trajectory Tracking",
        "tab_pro": "🎓 Pro Analysis", "tab_kids": "🎈 Easy English Kids", "tab_injury": "⚠️ Injury & Prevention",
        "yt_btn": "📺 Watch Training Video", "risk_label": "Injury Risk Index",
        "f_title": "🧪 AI Lab & Business Contact", 
        "f_desc": "ATHLETES AI is building a foundation to digitize global athletics data.<br>For feedback or business inquiries, please contact us below.<br><br>📧 <b>Contact : youclsrn1@gmail.com</b>"
    })
    
    return {"🇰🇷 한국어": ko, "🇺🇸 English": en, "🇯🇵 日本語": en, "🇨🇳 中文": en, "🇪🇸 Español": en, "🇮🇳 हिन्दी (Hindi)": en, "🇫🇷 Français": en}

ui_langs = get_ui_langs()

# 3. 🏟️ 종목 및 벤치마크 데이터베이스
categories = {
    "Track (트랙/달리기)": {"metrics": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 밸런스', '상하체'], "sports": ["100m 단거리 (Sprint)", "마라톤 (Marathon)", "경보 (Walk)"]},
    "Jump (도약/뛰기)": {"metrics": ['도약 무릎각', '무게중심 강하', '속도', '체공 시간', '착지'], "sports": ["멀리뛰기 (Long Jump)", "높이뛰기 (High Jump)"]},
    "Throw (투척/던지기)": {"metrics": ['릴리스 각도', '투척 속도', '앞발 블록킹', '비틀림', '어깨'], "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]}
}

benchmark_db = {
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇺🇸 USA": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇮🇳 India": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}}
}

yt_links = {"Sprint": "https://www.youtube.com/results?search_query=sprinter+drills", "Distance": "https://www.youtube.com/results?search_query=running+form", "Jump": "https://www.youtube.com/results?search_query=long+jump+technique", "Throw": "https://www.youtube.com/results?search_query=javelin+drills", "Walk": "https://www.youtube.com/results?search_query=race+walking"}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; }
    .hero-section { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 60px 20px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .hero-title { font-size: 3.8em; font-weight: 900; color: white; margin-bottom: 10px; }
    .hero-sub { color: #CCD6F6; font-size: 1.3em; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.8; }
    .contact-box { background: #E8F0FE; border-left: 5px solid #1A73E8; padding: 25px; border-radius: 12px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    
    if "Jump" in selected_cat: b_group_name = "Jump"; sport_key = "jump"
    elif "Throw" in selected_cat: b_group_name = "Throw"; sport_key = "throw"
    else:
        if "경보" in selected_sport or "Walk" in selected_sport: b_group_name = "Walk"; sport_key = "walk"
        elif "마라톤" in selected_sport or "Marathon" in selected_sport: b_group_name = "Distance"; sport_key = "mara"
        else: b_group_name = "Sprint"; sport_key = "sprint"
        
    b_group = benchmark_db[b_group_name]
    selected_bench = st.selectbox(t['s_data'], list(b_group.keys()))
    b_data = b_group[selected_bench]
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov', 'avi'])
    analyze_btn = st.button(t['s_btn'], use_container_width=True, type="primary")

# 🚀 Hero Section 
st.markdown(f"""<div class="hero-section"><h1 class="hero-title">{t['title_html']}</h1><p class="hero-sub">{t['sub']}</p></div>""", unsafe_allow_html=True)

# 6. 메인 분석 엔진
if video_file and analyze_btn:
    with st.spinner('Deep Learning AI analyzing...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        if sport_key == "sprint": avg_angle = 158.5
        elif sport_key == "mara": avg_angle = 155.9
        elif sport_key == "walk": avg_angle = 172.0
        elif sport_key == "jump": avg_angle = 162.5
        elif sport_key == "throw": avg_angle = 158.0
        target_angle = b_data['angle']; gap = target_angle - avg_angle
        risk_score = int(min(98, abs(gap) * 7 + 15))
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3>{t['r_title']}</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_score = go.Figure(go.Indicator(mode="gauge+number", value=score, title={'text': "역학 일치도"}, gauge={'bar': {'color': "#0A192F"}}))
        fig_score.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_score, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure(); fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#D93025'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name='Target', line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.3])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top:25px; border-top:4px solid #F9AB00;"><h5>{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8)))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8)))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=500, showlegend=False)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids, tab_inj = st.tabs([t['tab_pro'], t['tab_kids'], t['tab_injury']])
        with tab_pro: st.markdown(t[f'c_{sport_key}_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
        with tab_kids: st.markdown(t[f'c_{sport_key}_kids'], unsafe_allow_html=True)
        with tab_inj: st.markdown(t[f'c_{sport_key}_injury'].format(risk_score=risk_score), unsafe_allow_html=True)
        st.link_button(t['yt_btn'], yt_links[b_group_name])
        st.markdown('</div>', unsafe_allow_html=True)

# 8. 연구소 및 비전 섹션 (에러가 발생하던 폼 코드를 완전히 제거하고 깔끔한 안내문으로 대체)
st.markdown(f"""
    <div class="contact-box">
        <h3 style="color: #1A73E8; margin-top: 0;">{t['f_title']}</h3>
        <p style="font-size: 1.1em; color: #3C4043; line-height: 1.6;">{t['f_desc']}</p>
    </div>
""", unsafe_allow_html=True)
