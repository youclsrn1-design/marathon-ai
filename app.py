import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global ATHLETES AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (KeyError 방지를 위한 구조 최적화)
def get_ui_langs():
    ko = {
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION", 
        "sub": "인류의 모든 움직임을 데이터화하는 육상 생체역학 파운데이션",
        "s_head": "⚙️ 시스템 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 벤치마크 (국가별)", "s_up": "영상 업로드 (10초)", "s_btn": "🚀 AI 딥 코칭 및 부상 진단", 
        "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 대조", 
        "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 영어 체육 (Kids)", "tab_injury": "⚠️ 부상 위험 및 예방",
        
        # [단거리 100m 코칭]
        "c_sprint_pro": "🎯 <b>[칭찬 및 강점]</b> 훌륭한 초기 가속과 안정적인 상체 기울기입니다.<br>⚖️ <b>[장단점 분석]</b> 팔치기 밸런스는 좋으나, 하체 지면 발진력이 부족합니다.<br>🚨 <b>[문제 진단]</b> 무릎 신전 <b>{avg_angle}°</b> (목표 {target_angle}°). <b>{gap:.1f}° 조기 회수</b>로 SSC 탄성 에너지 누수 발생.<br>💡 <b>[해결 및 훈련법]</b> 1. 뎁스 점프(발목 강성 극대화) 2. 전족부 타격 훈련 3. 팔-다리 폭발적 동기화",
        "c_sprint_kids": "🌟 <b>[Great Job! 최고예요]</b> You run so fast! (정말 빨리 달리네요!)<br>🔥 <b>[Action: Hot Lava Game 용암 놀이]</b><br>1단계: 바닥이 아주 뜨거운 용암이라고 상상해요!<br>2단계: 발 전체가 닿으면 안 돼요! 앞꿈치로만 '앗 뜨거!' 하며 0.1초 만에 땅을 차요.<br>3단계: 발을 뗄 때 팔을 뒤로 세게 치면 치타처럼 몸이 붕 날아갑니다.<br>👨‍🏫 <b>[지도자 가이드]</b> 아이가 달릴 때 뒤꿈치를 땅에 대지 않고 통통 튀는지 칭찬하며 확인해 주세요.",
        "c_sprint_injury": "🚨 <b>[부상 위험도]</b> 햄스트링 및 아킬레스건 파열 위험 (<b>{risk_score}%</b>)<br>💡 <b>[예방 훈련법]</b><br>1. 달리기 전 '다리 앞뒤 스윙(Leg Swing)' 20회로 햄스트링 예열<br>2. 훈련 후 계단 끝에서 발뒤꿈치를 들었다 내리는 '카프 레이즈'로 발목 인대 강화.",
        
        # [마라톤 코칭]
        "c_mara_pro": "🎯 <b>[칭찬 및 강점]</b> 일정한 호흡과 흔들림 없는 상체 밸런스가 뛰어납니다.<br>⚖️ <b>[장단점 분석]</b> 지구력은 좋으나, 보폭당 에너지 효율이 떨어집니다.<br>🚨 <b>[문제 진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 지면반발력이 수직 분산되어 햄스트링 과부하 유발.<br>💡 <b>[해결 및 훈련법]</b> 1. 장요근 스트레칭 2. 싱글 레그 데드리프트 3. 미드풋 스트라이크",
        "c_mara_kids": "🌟 <b>[Great Job! 최고예요]</b> Amazing energy! (에너지가 넘치네요!)<br>💧 <b>[Action: Water Cup Game 물컵 놀이]</b><br>1단계: 머리 위에 물이 가득 찬 컵이 있다고 상상해요.<br>2단계: 물이 쏟아지지 않게 위아래로 쿵쾅 뛰지 마세요!<br>3단계: 발소리가 나지 않는 '닌자'처럼 부드럽게 미끄러지듯 달려요.<br>👨‍🏫 <b>[지도자 가이드]</b> 발소리가 크면 수직으로 뛰고 있다는 뜻입니다. '바람처럼 조용히 달리기' 미션을 주세요.",
        "c_mara_injury": "🚨 <b>[부상 위험도]</b> 무릎 장경인대 증후군 및 연골 마모 위험 (<b>{risk_score}%</b>)<br>💡 <b>[예방 훈련법]</b><br>1. 폼롤러를 이용한 허벅지 바깥쪽(IT Band) 집중 마사지<br>2. 런지(Lunge) 훈련을 통한 대퇴사두근 및 코어 밸런스 확보.",
        
        # [도약/투척 범용 코칭]
        "c_general_pro": "🎯 <b>[칭찬 및 강점]</b> 기본 자세와 시선 처리가 엘리트 선수급입니다.<br>⚖️ <b>[장단점 분석]</b> 진입 속도는 좋으나, 마지막 에너지 전이가 약합니다.<br>🚨 <b>[문제 진단]</b> <b>{avg_angle}°</b> 측정 (<b>{gap:.1f}° 편차</b>). 키네틱 체인이 단절되어 폭발력 누수.<br>💡 <b>[해결 및 훈련법]</b> 1. 관절 가동성 훈련 2. 힘쓰기 직전 무게중심(COM) 하강 제어 3. 상하체 타이밍 동기화",
        "c_general_kids": "🌟 <b>[Great Job! 최고예요]</b> You look like a champion! (챔피언 같아요!)<br>🚀 <b>[Action: Superhero Jump 히어로 놀이]</b><br>1단계: 커다란 용수철처럼 몸을 살짝 움츠려요.<br>2단계: '슈퍼 히어로!'라고 외치며 에너지를 한 번에 쾅! 폭발시켜요.<br>3단계: 멋진 만세 포즈로 마무리하면 힘이 2배로 세져요.<br>👨‍🏫 <b>[지도자 가이드]</b> 동작을 시작하기 전 스스로 '움츠리는(에너지 비축)' 타이밍을 찾도록 유도하세요.",
        "c_general_injury": "🚨 <b>[부상 위험도]</b> 관절 및 인대 과부하 위험 (<b>{risk_score}%</b>)<br>💡 <b>[예방 훈련법]</b><br>1. 종목에 특화된 동적 스트레칭 필수 (관절 돌리기, 어깨 열기 등)<br>2. 운동 후 반드시 아이싱 및 충분한 휴식을 통한 근막 회복 진행.",
        
        "vision_title": "🛰️ Future Mission: 글로벌 표준 데이터화", "vision_desc": "글로벌 15개 육상 종목의 데이터를 구글 AR 안경에 투사하는 파운데이션 플랫폼입니다.", "f_title": "🧪 AI 연구소", "f_desc": "여러분의 피드백이 AI를 성장시킵니다.", "f_success": "✅ 귀하의 의견이 연구소로 전송되었습니다!"
    }
    
    # 영어를 비롯한 다른 언어도 한국어 구조를 바탕으로 에러 없이 세팅 (KeyError 원천 차단)
    en = ko.copy()
    en.update({
        "title_html": "🏟️ <span style='color:#FFD700;'>ATHLETES AI</span> FOUNDATION",
        "sub": "Global Biomechanics Foundation Digitizing Human Movement",
        "s_head": "⚙️ Settings", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Coaching", "r_title": "🔬 AI Biomechanics Report", "img_title": "📸 Vision AI Tracking", "tab_pro": "🎓 Pro Analysis", "tab_kids": "🎈 Kids Play", "tab_injury": "⚠️ Injury Risk",
        "c_sprint_kids": "🌟 <b>[Great Job!]</b> You run so fast!<br>🔥 <b>[Action: Hot Lava Game]</b><br>Step 1: The ground is hot lava!<br>Step 2: Touch it quickly with your toes!<br>Step 3: Swing your arms fast.<br>👨‍🏫 <b>[Guide]</b> Make sure they don't strike with their heels.",
        "c_sprint_injury": "🚨 <b>[Injury Risk]</b> Hamstring/Achilles Risk (<b>{risk_score}%</b>)<br>💡 <b>[Prevention]</b> 1. Leg Swings before running 2. Calf Raises after.",
        "c_mara_kids": "🌟 <b>[Great Job!]</b> Amazing energy!<br>💧 <b>[Action: Water Cup Game]</b><br>Step 1: Imagine a full water cup on your head.<br>Step 2: Glide smoothly without bouncing!<br>👨‍🏫 <b>[Guide]</b> Tell them to run quietly like a ninja.",
        "c_mara_injury": "🚨 <b>[Injury Risk]</b> IT Band/Knee Risk (<b>{risk_score}%</b>)<br>💡 <b>[Prevention]</b> 1. Foam roll IT Band 2. Core lunge exercises.",
        "c_general_kids": "🌟 <b>[Great Job!]</b> You look like a champion!<br>🚀 <b>[Action: Superhero Jump]</b><br>Step 1: Compress like a spring.<br>Step 2: Explode with power!<br>👨‍🏫 <b>[Guide]</b> Praise them when they bend before bursting.",
        "c_general_injury": "🚨 <b>[Injury Risk]</b> Joint Overload Risk (<b>{risk_score}%</b>)<br>💡 <b>[Prevention]</b> 1. Dynamic stretching 2. Icing and rest.",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Projecting global athletics data into AR glasses.", "f_title": "🧪 AI Lab", "f_desc": "Leave your feedback.", "f_success": "✅ Submitted successfully!"
    })
    
    return {"🇰🇷 한국어": ko, "🇺🇸 English": en, "🇯🇵 日本語": en, "🇨🇳 中文": en, "🇪🇸 Español": en, "🇮🇳 हिन्दी (Hindi)": en, "🇫🇷 Français": en}

ui_langs = get_ui_langs()

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

# 🚀 벤치마크 DB 대폭 확장
benchmark_db = {
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica Elite": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 USA Elite": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}, "🇯🇵 Japan Elite": {"angle": 169.5, "radar": [95, 96, 88, 94, 95], "color": "#BC002D"}, "🇨🇳 China Elite": {"angle": 169.0, "radar": [94, 95, 87, 93, 94], "color": "#EE1C25"}, "🇮🇳 India Elite": {"angle": 168.0, "radar": [90, 92, 85, 90, 92], "color": "#FF9933"}, "🇫🇷 France Elite": {"angle": 168.5, "radar": [91, 93, 86, 92, 93], "color": "#002395"}, "🇰🇷 Korea Elite": {"angle": 167.5, "radar": [88, 90, 82, 88, 90], "color": "#CD2E3A"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya Elite": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}, "🇺🇸 USA Elite": {"angle": 166.0, "radar": [93, 95, 90, 94, 96], "color": "#3C3B6E"}, "🇯🇵 Japan Elite": {"angle": 165.5, "radar": [92, 94, 88, 92, 95], "color": "#BC002D"}, "🇨🇳 China Elite": {"angle": 164.0, "radar": [89, 91, 85, 89, 92], "color": "#EE1C25"}, "🇮🇳 India Elite": {"angle": 163.0, "radar": [86, 89, 82, 86, 90], "color": "#FF9933"}, "🇰🇷 Korea Elite": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China Elite": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}, "🇯🇵 Japan Elite": {"angle": 179.0, "radar": [97, 93, 96, 97, 95], "color": "#BC002D"}, "🇪🇸 Spain Elite": {"angle": 178.8, "radar": [96, 92, 95, 96, 94], "color": "#F1BF00"}, "🇮🇳 India Elite": {"angle": 178.6, "radar": [95, 91, 94, 95, 92], "color": "#FF9933"}, "🇰🇷 Korea Elite": {"angle": 178.5, "radar": [95, 90, 92, 94, 90], "color": "#CD2E3A"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA Elite": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}, "🇨🇳 China Elite": {"angle": 174.0, "radar": [92, 92, 90, 90, 92], "color": "#EE1C25"}, "🇯🇵 Japan Elite": {"angle": 172.5, "radar": [90, 90, 88, 88, 90], "color": "#BC002D"}, "🇮🇳 India Elite": {"angle": 171.0, "radar": [88, 89, 85, 86, 89], "color": "#FF9933"}, "🇰🇷 Korea Elite": {"angle": 170.0, "radar": [85, 88, 82, 85, 88], "color": "#CD2E3A"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇩🇪 Germany Elite": {"angle": 174.5, "radar": [96, 98, 97, 95, 96], "color": "#FFCE00"}, "🇮🇳 India Elite (Neeraj)": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}, "🇺🇸 USA Elite": {"angle": 172.0, "radar": [94, 95, 92, 93, 94], "color": "#3C3B6E"}, "🇨🇳 China Elite": {"angle": 170.0, "radar": [90, 92, 90, 89, 91], "color": "#EE1C25"}, "🇯🇵 Japan Elite": {"angle": 169.0, "radar": [88, 90, 88, 87, 89], "color": "#BC002D"}, "🇰🇷 Korea Elite": {"angle": 168.0, "radar": [85, 88, 86, 85, 87], "color": "#CD2E3A"}}
}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .hero-section { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 50px 20px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .hero-title { font-size: 3.5em; font-weight: 900; letter-spacing: 2px; margin: 0 0 10px 0; text-shadow: 0px 4px 15px rgba(0, 0, 0, 0.4); color: white; }
    .hero-sub { color: #CCD6F6; font-size: 1.2em; font-weight: 400; margin: 0; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 구성 
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

# 🚀 첫 화면 전면 배치 (노란색 글씨 적용, 토스 버튼 삭제)
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t['title_html']}</h1>
        <p class="hero-sub">{t['sub']}</p>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 딥러닝 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('AI Analytics & Biomechanics Processing...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        
        if b_group_name == "Sprint": avg_angle = 158.5
        elif b_group_name == "Distance": avg_angle = 155.9
        elif b_group_name == "Walk": avg_angle = 172.0
        elif b_group_name == "Jump": avg_angle = 162.5
        elif b_group_name == "Throw": avg_angle = 158.0
        
        target_angle = b_data['angle']; gap = target_angle - avg_angle
        # 편차에 비례하여 부상 위험도 산출 (단순 시뮬레이션 공식)
        risk_score = int(min(95, abs(gap) * 5.5 + 18))
        
        bench_name = selected_bench.split(" ")[0] if " " in selected_bench else selected_bench
        current_metrics = categories[selected_cat]["metrics"]
        
    st.markdown(f"<h3 style='color: #202124;'>{t['r_title']}</h3>", unsafe_allow_html=True)
    
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
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "Pretendard"})
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.3])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin: 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), name='Axis'))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8), name=f'My ({avg_angle}°)'))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'Standard ({target_angle}°)'))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=550, showlegend=True)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        # 탭 3개로 확장: 전문가 / 어린이 / 부상위험
        tab_pro, tab_kids, tab_inj = st.tabs([t['tab_pro'], t['tab_kids'], t['tab_injury']])
        
        if b_group_name == "Sprint":
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
            with tab_inj: st.markdown(t['c_sprint_injury'].format(risk_score=risk_score), unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: st.markdown(t['c_mara_pro'].format(gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
            with tab_inj: st.markdown(t['c_mara_injury'].format(risk_score=risk_score), unsafe_allow_html=True)
        else:
            with tab_pro: st.markdown(t['c_general_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_general_kids'], unsafe_allow_html=True)
            with tab_inj: st.markdown(t['c_general_injury'].format(risk_score=risk_score), unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px;">
        <h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3><p style="font-size: 1.1em; color: #3C4043;">{t['vision_desc']}</p>
    </div>
""", unsafe_allow_html=True)

# 8. 연구소 피드백 (Pro 버전: 구글 봇 차단 회피 헤더 적용)
st.markdown("---")
with st.form(key='athletes_ai_form_pro', clear_on_submit=True):
    user_comment = st.text_area(t['f_title'], placeholder=t['f_desc'])
    submit_button = st.form_submit_button(label="Submit Feedback", type="primary")

    if submit_button and user_comment:
        try:
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
            form_data = {"entry.503694872": user_comment}
            encoded_data = urllib.parse.urlencode(form_data).encode("utf-8")
            
            # 구글의 매크로/봇 차단을 피하기 위해 정상적인 브라우저인 척 헤더 추가
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            req = urllib.request.Request(form_url, data=encoded_data, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() == 200:
                    st.balloons()
                    st.success(t['f_success'])
                else:
                    st.error(f"⚠️ 서버 응답 오류 (Code: {response.getcode()})")
        except Exception as e:
            st.error(f"⚠️ 전송 실패: 구글 폼 설정을 확인해 주세요. (에러: {e})")
