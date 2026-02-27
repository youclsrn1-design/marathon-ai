import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =====================================================================
# 1. 시스템 환경 설정 (System Config)
# =====================================================================
st.set_page_config(page_title="ATHLETES AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# =====================================================================
# 2. 데이터베이스 & 다국어 캐싱 (Performance Optimization)
# =====================================================================
@st.cache_data
def load_language_packs():
    """글로벌 7대 언어팩 로드 (KeyError 원천 차단을 위한 Base Dict 구조화)"""
    
    # [BASE] 한국어 (모든 종목의 필수 Key를 100% 포함)
    base_ko = {
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION", 
        "sub": "글로벌 15개 육상 종목 생체역학 파운데이션 모델",
        "s_head": "⚙️ AI 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 국가별 벤치마크", 
        "s_up": "측면 영상 업로드", "s_btn": "🚀 AI 딥 코칭 & 부상 진단", 
        "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 대조", 
        "tab_pro": "🎓 전문가 분석", "tab_kids": "🎈 어린이 코칭", "tab_injury": "⚠️ 부상 위험 진단",
        "yt_btn": "📺 맞춤형 교정 훈련 영상",
        
        # 1. 단거리 (Sprint)
        "c_sprint_pro": "🎯 <b>[강점]</b> 초기 가속 시 상체 기울기 최상.<br>🚨 <b>[진단]</b> 무릎 신전 <b>{avg_angle}°</b>. <b>{gap:.1f}° 조기 회수</b>로 지면 반발력 누수.<br>💡 <b>[솔루션]</b> 뎁스 점프 및 전족부 타격 훈련.",
        "c_sprint_kids": "🌟 <b>[Praise]</b> 로켓처럼 빨라요!<br>🔥 <b>[Lava Game]</b> 1. 바닥이 용암이에요! 2. 앞꿈치로 0.1초 만에 땅을 차요! 3. 팔을 뒤로 치며 날아가요!",
        "c_sprint_injury": "🚨 <b>[부상 위험]</b> 햄스트링/아킬레스건 위험도 <b>{risk_score}%</b><br>🛠 <b>[예방]</b> 운동 전 레그 스윙 20회, 운동 후 카프 레이즈 필수.",
        
        # 2. 마라톤 (Distance)
        "c_mara_pro": "🎯 <b>[강점]</b> 일정한 호흡과 밸런스 유지 탁월.<br>🚨 <b>[진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 인한 수직 충격량 증가.<br>💡 <b>[솔루션]</b> 장요근 스트레칭 및 싱글 레그 데드리프트.",
        "c_mara_kids": "🌟 <b>[Praise]</b> 에너지가 넘치네요!<br>💧 <b>[Cup Game]</b> 1. 머리 위에 물컵이 있어요. 2. 쿵쾅 뛰지 말고 닌자처럼 부드럽게 달려요!",
        "c_mara_injury": "🚨 <b>[부상 위험]</b> 장경인대 및 무릎 연골 부하 <b>{risk_score}%</b><br>🛠 <b>[예방]</b> 측면 폼롤러 마사지 및 코어 런지.",

        # 3. 도약 (Jump)
        "c_jump_pro": "🎯 <b>[강점]</b> 진입 최고 속도 유지 탁월.<br>🚨 <b>[진단]</b> 도약 전 무게중심(COM) 하강 <b>{gap:.1f}° 편차</b>. 수직 에너지 전환율 저하.<br>💡 <b>[솔루션]</b> 펜울티메이트(Penultimate) 스텝 제어 훈련.",
        "c_jump_kids": "🌟 <b>[Praise]</b> 캥거루처럼 높이 뛰네요!<br>🚀 <b>[Hero Jump]</b> 1. 용수철처럼 움츠렸다가 2. '히어로!' 외치며 폭발해요!",
        "c_jump_injury": "🚨 <b>[부상 위험]</b> 발목 인대 및 슬개건 부하 <b>{risk_score}%</b><br>🛠 <b>[예방]</b> 착지 시 무릎 완충 작용 훈련 및 아이싱.",

        # 4. 투척 (Throw)
        "c_throw_pro": "🎯 <b>[강점]</b> 릴리스 시 상체 회전 타이밍 우수.<br>🚨 <b>[진단]</b> 앞발 블록킹 각도 <b>{gap:.1f}° 편차</b>. 하체 에너지가 상체로 전달 전 누수.<br>💡 <b>[솔루션]</b> 스탠딩 블록 훈련 및 코어 비틀림 강화.",
        "c_throw_kids": "🌟 <b>[Praise]</b> 힘이 엄청나네요!<br>🎯 <b>[Statue Game]</b> 1. 앞발을 '얼음!' 멈추고 2. 몸을 투석기처럼 휙 던져요!",
        "c_throw_injury": "🚨 <b>[부상 위험]</b> 어깨 회전근개/팔꿈치 과부하 <b>{risk_score}%</b><br>🛠 <b>[예방]</b> 흉추 가동성 스트레칭 및 밴드 회전근 강화.",

        # 5. 경보 (Walk)
        "c_walk_pro": "🎯 <b>[강점]</b> 골반의 수평 회전 리듬 완벽.<br>🚨 <b>[진단]</b> 무릎 완전 신전 부족 (<b>{gap:.1f}° 편차</b>). 파울 위험 구간 노출.<br>💡 <b>[솔루션]</b> 햄스트링 가동성 확보 및 뒤꿈치 롤링 훈련.",
        "c_walk_kids": "🌟 <b>[Praise]</b> 모델처럼 걷네요!<br>🚶‍♂️ <b>[Stick Game]</b> 1. 다리를 막대기처럼 쫙 펴고 2. 엉덩이를 씰룩이며 빠르게 걸어봐요!",
        "c_walk_injury": "🚨 <b>[부상 위험]</b> 고관절 마찰 및 햄스트링 긴장 <b>{risk_score}%</b><br>🛠 <b>[예방]</b> 장요근 스트레칭 및 둔근 활성화 운동.",

        "vision_title": "🛰️ Future Mission: 글로벌 스탠다드 연동", 
        "vision_desc": "2031년, 구글 AR 안경을 통해 전 세계인의 생체역학 데이터를 실시간으로 코칭하는 글로벌 파운데이션입니다.",
        "f_title": "🧬 AI LAB & PARTNERSHIP", 
        "f_desc": "서비스 고도화 및 비즈니스 제휴를 위한 피드백은 아래 이메일로 다이렉트 전송해 주십시오.",
        "btn_email": "✉️ 대표 이메일로 다이렉트 문의"
    }

    # [ENGLISH] 영어 베이스 설정 (Base Dict 상속 후 값 업데이트)
    en = base_ko.copy()
    en.update({
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION", "sub": "Global Biomechanics Prediction Foundation",
        "s_head": "⚙️ Configuration", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Diagnostic", 
        "r_title": "🔬 AI Biomechanics & Injury Report", "img_title": "📸 Vision AI Skeletal Tracking", 
        "tab_pro": "🎓 Pro Analysis", "tab_kids": "🎈 Kids Play", "tab_injury": "⚠️ Injury Risk", "yt_btn": "📺 Custom Drill Video",
        "c_sprint_pro": "🎯 <b>[Strength]</b> Excellent torso lean.<br>🚨 <b>[Diagnosis]</b> Knee ext <b>{avg_angle}°</b>. <b>{gap:.1f}° early recovery</b> causes SSC leak.<br>💡 <b>[Solution]</b> Depth jumps & forefoot striking.",
        "c_sprint_kids": "🌟 <b>[Praise]</b> Fast as a rocket!<br>🔥 <b>[Lava Game]</b> Touch the hot lava with toes and fly!", "c_sprint_injury": "🚨 <b>[Risk]</b> Hamstring Risk <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Dynamic leg swings & calf raises.",
        "c_mara_pro": "🎯 <b>[Strength]</b> Great breathing rhythm.<br>🚨 <b>[Diagnosis]</b> <b>{gap:.1f}° deviation</b>. Pelvic drop causing energy dispersion.<br>💡 <b>[Solution]</b> Iliopsoas stretch & midfoot striking.",
        "c_mara_kids": "🌟 <b>[Praise]</b> Amazing stamina!<br>💧 <b>[Cup Game]</b> Run smoothly like a ninja to keep the water cup safe!", "c_mara_injury": "🚨 <b>[Risk]</b> IT Band Risk <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Foam rolling & core lunges.",
        "c_jump_pro": "🎯 <b>[Strength]</b> Good approach speed.<br>🚨 <b>[Diagnosis]</b> COM drop lacks <b>{gap:.1f}°</b>.<br>💡 <b>[Solution]</b> Penultimate step control.", "c_jump_kids": "🌟 <b>[Praise]</b> High flyer!<br>🚀 <b>[Hero Jump]</b> Compress and explode!", "c_jump_injury": "🚨 <b>[Risk]</b> Ankle strain <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Knee buffering & icing.",
        "c_throw_pro": "🎯 <b>[Strength]</b> Clean arm swing.<br>🚨 <b>[Diagnosis]</b> Block leg deviation <b>{gap:.1f}°</b>.<br>💡 <b>[Solution]</b> Standing block drills.", "c_throw_kids": "🌟 <b>[Praise]</b> Power arm!<br>🎯 <b>[Statue Game]</b> Freeze front leg and throw!", "c_throw_injury": "🚨 <b>[Risk]</b> Rotator cuff risk <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Thoracic mobility.",
        "c_walk_pro": "🎯 <b>[Strength]</b> Good hip rotation.<br>🚨 <b>[Diagnosis]</b> Knee extension deviation <b>{gap:.1f}°</b>.<br>💡 <b>[Solution]</b> Heel rolling drills.", "c_walk_kids": "🌟 <b>[Praise]</b> Cool walker!<br>🚶‍♂️ <b>[Stick Game]</b> Keep legs straight!", "c_walk_injury": "🚨 <b>[Risk]</b> Hip friction <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Glute activation.",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Real-time AR Biomechanics Coaching.", "f_title": "🧬 AI LAB & CONTACT", "f_desc": "Send us your feedback directly via email.", "btn_email": "✉️ Contact CEO via Email"
    })

    return {"🇰🇷 한국어": base_ko, "🇺🇸 English": en, "🇯🇵 日本語": en, "🇨🇳 中文": en, "🇪🇸 Español": en, "🇮🇳 हिन्दी (Hindi)": en, "🇫🇷 Français": en}

@st.cache_data
def load_databases():
    """카테고리 및 벤치마크 DB 최적화 로드"""
    cats = {
        "Track (트랙/달리기)": {"metrics": ['무릎 신전(Knee Ext)', '지면접촉(GCT)', '수직진폭(Oscillation)', '골반 밸런스(Pelvic)', '상하체 동기화(Sync)'], "sports": ["100m 단거리 (Sprint)", "마라톤 (Marathon)", "경보 (Walk)"]},
        "Jump (도약/뛰기)": {"metrics": ['도약 무릎각(Take-off)', '무게중심 강하(COM Drop)', '진입 속도(Approach)', '체공 시간(Flight)', '착지 안정성(Landing)'], "sports": ["멀리뛰기 (Long Jump)", "높이뛰기 (High Jump)", "장대높이뛰기 (Pole Vault)"]},
        "Throw (투척/던지기)": {"metrics": ['릴리스 팔각도(Release)', '투척 속도(Velocity)', '앞발 블록킹(Blocking)', '몸통 비틀림(Trunk)', '어깨 회전축(Shoulder)'], "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]}
    }
    bench = {
        "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica Elite": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 USA Elite": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}},
        "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya Elite": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}},
        "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China Elite": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}},
        "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA Elite": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}},
        "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇮🇳 India Elite": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}}
    }
    yt = {"Sprint": "sprinter+drills", "Distance": "running+form+correction", "Jump": "long+jump+technique", "Throw": "javelin+throw+drills", "Walk": "race+walking+technique"}
    return cats, bench, yt

ui_langs = load_language_packs()
categories, benchmark_db, yt_links = load_databases()

# =====================================================================
# 3. 프론트엔드 스타일링 (Enterprise UI/UX)
# =====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #1F2937; }
    .hero-container { background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #374151 100%); padding: 50px 20px; border-radius: 16px; text-align: center; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.2); }
    .hero-title { font-size: 3.5em; font-weight: 900; letter-spacing: 1px; color: #F3F4F6; margin-bottom: 8px; }
    .hero-sub { color: #9CA3AF; font-size: 1.2em; font-weight: 400; }
    .card-panel { background: #FFFFFF; padding: 25px; border-radius: 16px; border: 1px solid #E5E7EB; box-shadow: 0 4px 15px rgba(0,0,0,0.02); height: 100%; }
    .coach-panel { background: #FFFFFF; border-top: 5px solid #2563EB; padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); height: 100%; line-height: 1.6; }
    .contact-card { background: #EFF6FF; border-left: 5px solid #2563EB; padding: 30px; border-radius: 12px; margin-top: 30px; }
    .email-btn { display: inline-block; background: #2563EB; color: white !important; font-weight: bold; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 10px; transition: 0.3s; }
    .email-btn:hover { background: #1D4ED8; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 4. 사이드바 & 입력 컨트롤 (Sidebar Controls)
# =====================================================================
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    
    # 종목 키맵핑 (O(1) 검색 최적화)
    if "Jump" in selected_cat: b_group_name, sport_key = "Jump", "jump"
    elif "Throw" in selected_cat: b_group_name, sport_key = "Throw", "throw"
    elif "Walk" in selected_sport or "경보" in selected_sport: b_group_name, sport_key = "Walk", "walk"
    elif "Marathon" in selected_sport or "마라톤" in selected_sport: b_group_name, sport_key = "Distance", "mara"
    else: b_group_name, sport_key = "Sprint", "sprint"
        
    b_group = benchmark_db[b_group_name]
    selected_bench = st.selectbox(t['s_data'], list(b_group.keys()))
    b_data = b_group[selected_bench]
    
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov'])
    analyze_btn = st.button(t['s_btn'], use_container_width=True, type="primary")

# =====================================================================
# 5. 메인 레이아웃 및 렌더링 (Main Render)
# =====================================================================
st.markdown(f"""<div class="hero-container"><h1 class="hero-title">{t['title_html']}</h1><p class="hero-sub">{t['sub']}</p></div>""", unsafe_allow_html=True)

if video_file and analyze_btn:
    with st.spinner('Pro Engine Analyzing Biomechanics...'):
        # 시뮬레이션 엔진 로직
        score = 78; my_stats = [75, 68, 85, 70, 65]
        angle_map = {"sprint": 158.5, "mara": 155.9, "walk": 172.0, "jump": 162.5, "throw": 158.0}
        avg_angle = angle_map[sport_key]
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        risk_score = int(min(98, abs(gap) * 6 + 12))
        bench_name = selected_bench.split(" ")[0] if " " in selected_bench else selected_bench
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3 style='color: #1F2937; margin-bottom: 20px;'>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    # 상단 차트 영역 (게이지 & 레이더)
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1F2937"}, 'steps': [{'range': [0, 75], 'color': "#F3F4F6"}, {'range': [85, 100], 'color': "#D1FAE5"}]}))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card-panel">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#EF4444'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=280, margin=dict(l=50, r=50, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "Pretendard"})
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 하단 코칭 영역 (비전 궤적 & 텍스트 리포트)
    col3, col4 = st.columns([1, 1.3])
    with col3:
        st.markdown(f"""<div class="card-panel" style="margin-top: 25px; border-top: 4px solid #FFD700;"><h5 style="color: #1F2937; margin: 0 0 10px 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='#9CA3AF', width=8), name='고정축'))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#EF4444', width=8), name=f'My 궤적'))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#10B981', width=4, dash='dot'), name=f'Target'))
        fig_ov.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=10, r=10, t=10, b=10), height=520, showlegend=False)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coach-panel" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids, tab_inj = st.tabs([t['tab_pro'], t['tab_kids'], t['tab_injury']])
        
        # 동적 키 호출 로직 (에러 발생 불가능)
        with tab_pro: 
            st.markdown(t[f'c_{sport_key}_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
        with tab_kids: 
            st.markdown(t[f'c_{sport_key}_kids'], unsafe_allow_html=True)
        with tab_inj: 
            st.markdown(t[f'c_{sport_key}_injury'].format(risk_score=risk_score), unsafe_allow_html=True)
            
        st.link_button(t['yt_btn'], f"https://www.youtube.com/results?search_query={yt_links[b_group_name]}")
        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
# 6. 비전 및 다이렉트 이메일 컨택 (Business Section)
# =====================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="background: linear-gradient(to right, #EFF6FF, #FFFFFF); border-left: 5px solid #2563EB; padding: 30px; border-radius: 12px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">{t['vision_title']}</h3>
        <p style="font-size: 1.1em; color: #4B5563;">{t['vision_desc']}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
    <div class="contact-card">
        <h3 style="color: #1E3A8A; margin-top: 0;">{t['f_title']}</h3>
        <p style="font-size: 1.1em; color: #4B5563; margin-bottom: 20px;">{t['f_desc']}</p>
        <a href="mailto:youclsrn1@gmail.com?subject=[ATHLETES AI 피드백/제휴 문의]" class="email-btn">{t['btn_email']}</a>
    </div>
""", unsafe_allow_html=True)
