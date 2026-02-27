import streamlit as st
import numpy as np
import plotly.graph_objects as go
import re

# =====================================================================
# 1. 시스템 환경 설정 (V31.0 - 400mH & Audio TTS Edition)
# =====================================================================
st.set_page_config(page_title="ATHLETES AI | Global Foundation", layout="wide", initial_sidebar_state="expanded")

# =====================================================================
# 2. 다국어 팩 (에러 0% 방어벽 유지 + 400mH 데이터 추가)
# =====================================================================
@st.cache_data
def load_language_packs():
    base_ko = {
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION", 
        "sub": "글로벌 15개 육상 종목 생체역학 파운데이션 모델",
        "s_head": "⚙️ AI 분석 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 국가별 벤치마크", 
        "s_up": "측면 폼 영상 업로드", "s_btn": "🚀 AI 딥 코칭 & 부상 예측", 
        "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 트래킹", 
        "tab_pro": "🎓 전문가 분석", "tab_kids": "🎈 어린이 코칭", "tab_injury": "⚠️ 부상 위험 예측",
        "yt_btn": "📺 내게 맞는 훈련 영상 보기",
        
        # [단거리 - Sprint]
        "c_sprint_pro": "🎯 <b>[강점]</b> 초기 가속 시 상체 기울기 최상.<br>🚨 <b>[진단]</b> 무릎 신전 <b>{avg_angle}°</b>. 목표 대비 <b>{gap:.1f}° 조기 회수</b>로 지면 반발력 누수.<br>💡 <b>[솔루션]</b> 뎁스 점프 및 전족부 타격 훈련.",
        "c_sprint_kids": "🌟 <b>[Praise]</b> 로켓처럼 빨라요!<br>🔥 <b>[용암 놀이]</b> 1. 바닥이 뜨거운 용암이에요! 2. 앞꿈치로 0.1초 만에 차요! 3. 팔을 뒤로 치며 날아가요!",
        "c_sprint_injury": "🚨 <b>[부상 위험]</b> 햄스트링/아킬레스건 위험 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 운동 전 레그 스윙 20회, 훈련 후 카프 레이즈 필수.",
        
        # [마라톤 - Distance]
        "c_mara_pro": "🎯 <b>[강점]</b> 일정한 호흡과 흔들림 없는 밸런스 탁월.<br>🚨 <b>[진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 인한 수직 에너지 분산.<br>💡 <b>[솔루션]</b> 장요근 스트레칭 및 싱글 레그 데드리프트 훈련.",
        "c_mara_kids": "🌟 <b>[Praise]</b> 에너지가 넘치네요!<br>💧 <b>[물컵 놀이]</b> 1. 머리에 물컵이 있어요. 2. 물이 쏟아지지 않게 닌자처럼 부드럽게 달려요!",
        "c_mara_injury": "🚨 <b>[부상 위험]</b> 장경인대(IT Band) 증후군 위험 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 폼롤러 측면 마사지 및 코어 런지 훈련.",

        # [400m 허들 - Hurdle] (신규 추가)
        "c_hurdle_pro": "🎯 <b>[강점]</b> 허들링 구간 진입 속도와 리드 레그(Lead Leg) 확장이 훌륭합니다.<br>🚨 <b>[진단]</b> 트레일 레그(Trail Leg) 회수 각도 <b>{gap:.1f}° 편차</b>. 착지 후 감속폭이 큽니다.<br>💡 <b>[솔루션]</b> 고관절 가동성 훈련 및 허들 측면 넘기 드릴(Drill).",
        "c_hurdle_kids": "🌟 <b>[Praise]</b> 장애물을 훌쩍 넘는 모습이 멋져요!<br>🚀 <b>[가위 놀이]</b> 1. 종이상자를 두고 2. 다리를 가위처럼 쫙 벌려서 3. 새처럼 날아가봐요!",
        "c_hurdle_injury": "🚨 <b>[부상 위험]</b> 햄스트링 및 고관절 굴곡근 파열 위험 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 허들 전용 고관절 동적 스트레칭 및 골반 열기 필수.",

        # [도약 - Jump]
        "c_jump_pro": "🎯 <b>[강점]</b> 진입 최고 속도 유지 및 시선 처리 탁월.<br>🚨 <b>[진단]</b> 도약 전 무게중심 하강 <b>{gap:.1f}° 편차</b>. 수직 에너지 전환율 저하.<br>💡 <b>[솔루션]</b> 펜울티메이트(Penultimate) 스텝 제어 훈련.",
        "c_jump_kids": "🌟 <b>[Praise]</b> 캥거루처럼 높이 뛰네요!<br>🚀 <b>[히어로 점프]</b> 1. 용수철처럼 웅크렸다가 2. '히어로!' 외치며 팡 터트려요!",
        "c_jump_injury": "🚨 <b>[부상 위험]</b> 발목 인대 및 슬개건 부하 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 착지 시 무릎 완충 작용 집중 훈련 및 아이싱.",

        # [투척 - Throw]
        "c_throw_pro": "🎯 <b>[강점]</b> 릴리스 시 상체 회전 타이밍 우수.<br>🚨 <b>[진단]</b> 앞발 블록킹 각도 <b>{gap:.1f}° 편차</b>. 하체 에너지가 상체로 가기 전 누수.<br>💡 <b>[솔루션]</b> 스탠딩 블록 훈련 및 코어 비틀림 강화.",
        "c_throw_kids": "🌟 <b>[Praise]</b> 파워가 엄청나네요!<br>🎯 <b>[얼음 놀이]</b> 1. 앞발을 '얼음!' 멈추고 2. 몸을 투석기처럼 휙 던져요!",
        "c_throw_injury": "🚨 <b>[부상 위험]</b> 어깨 회전근개 과부하 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 흉추 가동성 스트레칭 및 밴드 운동.",

        # [경보 - Walk]
        "c_walk_pro": "🎯 <b>[강점]</b> 골반 수평 회전 리듬 완벽.<br>🚨 <b>[진단]</b> 무릎 신전 <b>{gap:.1f}° 편차</b>. 파울 판정 위험 구간 노출.<br>💡 <b>[솔루션]</b> 햄스트링 가동성 확보 및 뒤꿈치 롤링 훈련.",
        "c_walk_kids": "🌟 <b>[Praise]</b> 모델처럼 멋지게 걷네요!<br>🚶‍♂️ <b>[막대기 놀이]</b> 1. 다리를 막대기처럼 펴고 2. 엉덩이를 씰룩이며 빠르게 걸어요!",
        "c_walk_injury": "🚨 <b>[부상 위험]</b> 고관절 마찰 및 긴장 (<b>{risk_score}%</b>)<br>🛠 <b>[예방]</b> 장요근 스트레칭 및 둔근 활성화.",

        "vision_title": "🛰️ Future Mission: 글로벌 데이터 연동", 
        "vision_desc": "2031년, AR 안경을 통해 전 세계 러너들의 자세를 실시간으로 교정하는 글로벌 인프라가 됩니다.",
        "f_title": "🧬 AI LAB & PARTNERSHIP", 
        "f_desc": "서비스 고도화 및 비즈니스 제휴를 위한 피드백은 아래 이메일로 다이렉트 전송해 주십시오.",
        "btn_email": "✉️ 대표 이메일로 피드백 보내기 (youclsrn1@gmail.com)"
    }

    # 영어를 비롯한 타 언어 팩 자동 생성 (에러 완벽 방어)
    en = base_ko.copy()
    en.update({
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION", "sub": "Global Biomechanics Prediction Foundation",
        "s_head": "⚙️ AI Config", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Target Benchmark", 
        "s_up": "Upload Video", "s_btn": "🚀 Run AI Diagnostic", "r_title": "🔬 AI Biomechanics & Injury Report", 
        "img_title": "📸 Vision AI Skeletal Tracking", "tab_pro": "🎓 Pro Analysis", "tab_kids": "🎈 Kids Play", "tab_injury": "⚠️ Injury Risk",
        "c_hurdle_pro": "🎯 <b>[Strength]</b> Great lead leg extension.<br>🚨 <b>[Diagnosis]</b> Trail leg deviation <b>{gap:.1f}°</b>.<br>💡 <b>[Solution]</b> Hip mobility & hurdle drills.",
        "c_hurdle_kids": "🌟 <b>[Praise]</b> Great jump!<br>🚀 <b>[Scissor Game]</b> Open your legs like scissors and fly!",
        "c_hurdle_injury": "🚨 <b>[Risk]</b> Hamstring Risk <b>{risk_score}%</b><br>🛠 <b>[Prevention]</b> Dynamic hip stretching.",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Real-time AR Biomechanics Coaching.",
        "f_title": "🧬 AI LAB & CONTACT", "f_desc": "Send us your feedback directly via email to upgrade the AI.", "btn_email": "✉️ Contact via Email"
    })
    
    return {"🇰🇷 한국어": base_ko, "🇺🇸 English": en, "🇯🇵 日本語": en, "🇨🇳 中文": en, "🇪🇸 Español": en, "🇮🇳 हिन्दी (Hindi)": en, "🇫🇷 Français": en}

@st.cache_data
def load_databases():
    # 400m 허들 종목 및 허들 벤치마크 추가
    cats = {
        "Track (트랙/달리기)": {"metrics": ['무릎 신전(Knee)', '지면접촉(GCT)', '수직진폭(Bounce)', '골반 밸런스(Pelvic)', '상하체 동기화(Sync)'], "sports": ["100m 단거리 (Sprint)", "400m 허들 (400mH)", "마라톤 (Marathon)", "경보 (Walk)"]},
        "Jump (도약/뛰기)": {"metrics": ['도약각(Take-off)', '중심강하(Drop)', '진입속도(Speed)', '체공시간(Flight)', '착지안정성(Land)'], "sports": ["멀리뛰기 (Long Jump)", "높이뛰기 (High Jump)"]},
        "Throw (투척/던지기)": {"metrics": ['릴리스(Release)', '투척속도(Velocity)', '앞발블록(Block)', '몸통비틀림(Trunk)', '어깨회전(Shoulder)'], "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]}
    }
    
    bench = {
        "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica Elite": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 USA Elite": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}},
        "Hurdle": { # 400mH 전용 국가별 벤치마크 (발홀름 등 추가)
            "🌍 World Record (Warholm)": {"angle": 165.0, "radar": [98, 96, 99, 94, 98], "color": "#000000"},
            "🇳🇴 Norway Elite": {"angle": 164.5, "radar": [97, 95, 98, 95, 97], "color": "#BA0C2F"},
            "🇺🇸 USA Elite (Sydney)": {"angle": 166.0, "radar": [96, 96, 97, 96, 95], "color": "#3C3B6E"}
        },
        "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya Elite": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}, "🇰🇷 Korea Elite": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#1A73E8"}},
        "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China Elite": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}},
        "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA Elite": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}},
        "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇮🇳 India Elite": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}}
    }
    yt = {"Sprint": "sprinter+drills", "Hurdle": "400m+hurdles+technique", "Distance": "marathon+running+form", "Jump": "long+jump+technique", "Throw": "javelin+throw+drills", "Walk": "race+walking+technique"}
    return cats, bench, yt

ui_langs = load_language_packs()
categories, benchmark_db, yt_links = load_databases()

# =====================================================================
# 3. 고급 프론트엔드 스타일 (V30.0 디자인 100% 유지)
# =====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F3F4F6; color: #1F2937; }
    .hero-container { background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #374151 100%); padding: 50px 20px; border-radius: 16px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    .hero-title { font-size: 3.5em; font-weight: 900; letter-spacing: 1px; color: #F9FAFB; margin-bottom: 5px; }
    .hero-sub { color: #D1D5DB; font-size: 1.2em; font-weight: 400; }
    .card-panel { background: #FFFFFF; padding: 25px; border-radius: 16px; border: 1px solid #E5E7EB; box-shadow: 0 4px 15px rgba(0,0,0,0.03); height: 100%; }
    .coach-panel { background: #FFFFFF; border-top: 5px solid #2563EB; padding: 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); height: 100%; line-height: 1.7; }
    .email-btn { display: inline-block; background: #2563EB; color: white !important; font-weight: bold; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 10px; transition: 0.2s; }
    .email-btn:hover { background: #1D4ED8; }
    .audio-btn { display: inline-block; background: #10B981; color: white !important; font-weight: bold; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 15px; border: none; cursor: pointer; transition: 0.2s; font-size: 1em;}
    .audio-btn:hover { background: #059669; }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 4. 사이드바 제어 패널 (400mH 라우팅 추가)
# =====================================================================
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    selected_cat = st.selectbox(t.get('s_cat', '카테고리'), list(categories.keys()))
    selected_sport = st.selectbox(t.get('s_sport', '세부 종목'), categories[selected_cat]["sports"])
    
    # 400mH 허들 인식 로직 추가
    if "Jump" in selected_cat: b_group_name, sport_key = "Jump", "jump"
    elif "Throw" in selected_cat: b_group_name, sport_key = "Throw", "throw"
    elif "Walk" in selected_sport or "경보" in selected_sport: b_group_name, sport_key = "Walk", "walk"
    elif "Marathon" in selected_sport or "마라톤" in selected_sport: b_group_name, sport_key = "Distance", "mara"
    elif "400mH" in selected_sport or "허들" in selected_sport: b_group_name, sport_key = "Hurdle", "hurdle"
    else: b_group_name, sport_key = "Sprint", "sprint"
        
    b_group = benchmark_db[b_group_name]
    selected_bench = st.selectbox(t.get('s_data', '벤치마크'), list(b_group.keys()))
    b_data = b_group[selected_bench]
    
    st.markdown("---")
    video_file = st.file_uploader(t.get('s_up', '업로드'), type=['mp4', 'mov'])
    analyze_btn = st.button(t.get('s_btn', '분석 실행'), use_container_width=True, type="primary")

# =====================================================================
# 5. 메인 화면 렌더링
# =====================================================================
st.markdown(f"""<div class="hero-container"><h1 class="hero-title">{t.get('title_html', '')}</h1><p class="hero-sub">{t.get('sub', '')}</p></div>""", unsafe_allow_html=True)

if video_file and analyze_btn:
    with st.spinner('AI Biomechanics Processing...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        # 허들 고유 시뮬레이션 각도(160.5) 추가
        angle_map = {"sprint": 158.5, "hurdle": 160.5, "mara": 155.9, "walk": 172.0, "jump": 162.5, "throw": 158.0}
        avg_angle = angle_map[sport_key]
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        risk_score = int(min(98, abs(gap) * 6 + 12))
        bench_name = selected_bench.split(" ")[0] if " " in selected_bench else selected_bench
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3 style='color: #1F2937;'>{t.get('r_title', '')}</h3>", unsafe_allow_html=True)
    
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

    col3, col4 = st.columns([1, 1.3])
    with col3:
        st.markdown(f"""<div class="card-panel" style="margin-top: 25px; border-top: 4px solid #FFD700;"><h5 style="color: #1F2937; margin: 0;">{t.get('img_title', '')}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='#9CA3AF', width=8)))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#EF4444', width=8)))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#10B981', width=4, dash='dot')))
        fig_ov.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=10, r=10, t=10, b=10), height=520, showlegend=False)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coach-panel" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids, tab_inj = st.tabs([t.get('tab_pro', 'Pro'), t.get('tab_kids', 'Kids'), t.get('tab_injury', 'Injury')])
        
        # 텍스트 로드
        pro_text = t.get(f'c_{sport_key}_pro', '').format(avg_angle=avg_angle, target_angle=target_angle, gap=gap)
        kids_text = t.get(f'c_{sport_key}_kids', '')
        inj_text = t.get(f'c_{sport_key}_injury', '').format(risk_score=risk_score)
        
        # 오디오 스크립트용 클린 텍스트 (태그 제거)
        clean_text = re.sub(r'<[^>]+>', ' ', pro_text).replace('🎯', '').replace('🚨', '').replace('💡', '').replace("'", "")
        
        with tab_pro: 
            st.markdown(pro_text, unsafe_allow_html=True)
            # Web Speech API를 활용한 오디오 버튼 탑재 (서버 비용 0원)
            st.markdown(f"""
                <button onclick="
                    if('speechSynthesis' in window) {{
                        var msg = new SpeechSynthesisUtterance('{clean_text}');
                        window.speechSynthesis.speak(msg);
                    }} else {{ alert('오디오를 지원하지 않는 브라우저입니다.'); }}
                " class="audio-btn">🔊 오디오 코칭 듣기</button>
            """, unsafe_allow_html=True)
            
        with tab_kids: st.markdown(kids_text, unsafe_allow_html=True)
        with tab_inj: st.markdown(inj_text, unsafe_allow_html=True)
            
        st.link_button(t.get('yt_btn', 'YouTube'), f"https://www.youtube.com/results?search_query={yt_links.get(b_group_name, 'athletics+drills')}")
        st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
# 6. 하단 비즈니스 컨택트 보드 (이메일 유지)
# =====================================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="background: #EFF6FF; border-left: 5px solid #2563EB; padding: 30px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">{t.get('vision_title', '')}</h3>
        <p style="font-size: 1.1em; color: #4B5563;">{t.get('vision_desc', '')}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E5E7EB; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <h3 style="color: #1F2937; margin-top: 0;">{t.get('f_title', '')}</h3>
        <p style="font-size: 1.1em; color: #6B7280; margin-bottom: 20px;">{t.get('f_desc', '')}</p>
        <a href="mailto:youclsrn1@gmail.com?subject=[ATHLETES AI 피드백/제휴 문의]" class="email-btn">{t.get('btn_email', '')}</a>
    </div>
""", unsafe_allow_html=True)
