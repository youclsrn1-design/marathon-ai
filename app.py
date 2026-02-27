import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (코칭 텍스트 대폭 강화)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "글로벌 육상 전 종목 생체역학 교육 시스템", "toss": "Toss ID: ATHLETICS AI", "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 비교 벤치마크 (국가별)", "s_up": "측면 영상 파일 선택 (10초 이내)", "s_btn": "🚀 AI 정밀 분석 및 지도법 생성", "r_title": "🔬 생체역학 진단 및 교육 리포트", "img_title": "📸 비전 AI 관절 추출 및 종목별 궤적 대조", "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 훈련 지도법", "vision_title": "🛰️ Future Mission: 인류의 모든 움직임을 데이터화하다", "vision_desc": "마라톤, 100m, 창던지기 등 육상 15개 전 종목의 국가별 생체역학 DB를 스마트 안경(AR)에 실시간 투사하는 파운데이션 모델입니다.", "f_title": "🧪 ATHLETICS 연구소", "f_desc": "당신의 의견이 더 똑똑한 AI 코치를 만듭니다.", "f_success": "✅ 의견이 AI 연구소로 성공적으로 전송되었습니다!",
        
        # [단거리 텍스트 보강]
        "c_sprint_pro": "<b>[역학 진단: 지면 발진력 누수]</b><br>도약 시 무릎 신전 각도({avg_angle}°)가 엘리트({target_angle}°) 대비 <span style='color:#D93025; font-weight:bold;'>{gap:.1f}° 부족</span>합니다. 이는 발이 지면에 닿을 때 발목 배측굴곡(Dorsiflexion)이 무너지며, 아킬레스건의 SSC(신장-단축 주기) 탄성 에너지가 전진 가속도로 전환되지 못하고 흡수되어 버리는 현상입니다.<br><br><b>[교정 프로토콜]</b><br>1. <b>플라이오메트릭:</b> 뎁스 점프(Depth Jump)로 지면 접촉 시간(GCT) 최소화 및 발목 강성 확보<br>2. <b>A-Skip 훈련:</b> 전족부(발볼)로 수직 타격하며 햄스트링 빠른 회수 연습<br>3. <b>팔치기 동기화:</b> 지면 발진과 동시에 반대쪽 팔꿈치를 뒤로 강하게 끊어 치기", 
        "c_sprint_kids": "<b>[🔥 미션: 뜨거운 용암 밟기!]</b><br>바닥이 아주 뜨거운 용암이라고 상상해 봐요! 발바닥 전체가 닿으면 화상을 입어요.<br><br><b>1단계:</b> 뒤꿈치를 살짝 들고 앞꿈치로만 '앗 뜨거!' 하면서 0.1초 만에 발을 떼세요.<br><b>2단계:</b> 발을 뗄 때 팔꿈치를 뒤로 휙! 치면 치타처럼 로켓 출발을 할 수 있어요!<br><b>3단계:</b> 땅을 세게 밟을수록 몸이 더 가볍게 붕~ 날아가는 걸 느껴보세요.",
        
        # [마라톤 텍스트 보강]
        "c_mara_pro": "<b>[역학 진단: 수직 진폭 및 에너지 누수]</b><br>고관절과 무릎의 완전 신전(Triple Extension)이 이루어지지 않아 <span style='color:#D93025; font-weight:bold;'>{gap:.1f}°의 편차</span>가 발생합니다. 이는 골반 드롭(Pelvic Drop)과 결합되어 지면반발력(GRF)이 전진하는 수평 에너지가 아닌 수직으로 분산되는 비효율을 초래하며 햄스트링 과부하의 원인이 됩니다.<br><br><b>[교정 프로토콜]</b><br>1. <b>장요근 가동성:</b> 동적 스트레칭으로 고관절 후방 신전 가동 범위 물리적 확장<br>2. <b>코어 안정화:</b> 싱글 레그 데드리프트를 통한 중둔근 밸런스 확보<br>3. <b>미드풋 스트라이크:</b> 무게중심 바로 아래에 발을 디뎌 브레이킹 포스 최소화", 
        "c_mara_kids": "<b>[💧 미션: 닌자의 물컵 지키기!]</b><br>머리 위에 가득 찬 물컵이 있다고 상상해 봐요! 쿵쾅쿵쾅 뛰면 물이 다 쏟아지겠죠?<br><br><b>1단계:</b> 위아래로 폴짝폴짝 뛰지 말고, 자전거 페달을 돌리듯 발을 둥글게 굴려보세요.<br><b>2단계:</b> 뒤에서 바람이 날 밀어준다고 생각하고 상체를 살짝 앞으로 기울이세요.<br><b>3단계:</b> 발소리가 나지 않게 사뿐사뿐 닌자처럼 달리면 물을 한 방울도 안 흘릴 수 있어요!",
        
        # [도약 텍스트 보강]
        "c_jump_pro": "<b>[역학 진단: 수직 충격량 전환 실패]</b><br>도약 전 마지막 두 걸음(Penultimate Step)에서 무게중심(COM) 하강비가 부족해 발구름 각도가 <span style='color:#D93025; font-weight:bold;'>{avg_angle}°</span>에 그쳤습니다. 수평 진입 속도가 수직 충격량(Vertical Impulse)으로 전환되지 못하고 튕겨 나가고 있습니다.<br><br><b>[교정 프로토콜]</b><br>1. <b>힌지 제어:</b> 마지막 걸음에서 고관절 힌지를 통한 의도적 COM 하강 훈련<br>2. <b>아모티제이션:</b> 지면 접촉 후 즉각적인 족저근막 탄성 방출 연습<br>3. <b>상향 스윙:</b> 리드 암과 리드 레그의 폭발적인 상향 구동 매칭", 
        "c_jump_kids": "<b>[🚀 미션: 슈퍼 마리오 점프!]</b><br>점프하기 직전의 마지막 한 걸음이 가장 중요해요! 용수철처럼 몸을 압축해 봐요.<br><br><b>1단계:</b> 달려가다가 뛰기 직전 한 걸음에서 무릎을 평소보다 더 굽히고 몸을 낮추세요.<br><b>2단계:</b> 발이 땅에 닿는 순간 '쾅!' 소리가 나게 밟고, 마리오처럼 솟아오르세요!<br><b>3단계:</b> 뛰면서 양팔을 하늘 위로 펀치 하듯 뻗으면 훨씬 높이 날아가요.",
        
        # [투척 텍스트 보강]
        "c_throw_pro": "<b>[역학 진단: 키네틱 체인 붕괴]</b><br>리드 레그의 앞발 블록킹(Blocking) 동작이 무너져 <span style='color:#D93025; font-weight:bold;'>{gap:.1f}°의 편차</span>가 발생. 하체의 선운동량이 상체의 각운동량으로 전이되는 키네틱 체인(Kinetic Chain)이 단절되어 투척 에너지를 상실했습니다.<br><br><b>[교정 프로토콜]</b><br>1. <b>브레이싱(Bracing):</b> 블록킹 발 접지 시 무릎 관절을 100% 락킹(Locking)하는 정지 훈련<br>2. <b>X-Factor:</b> 흉추 가동성 극대화를 통한 하체-코어 역학적 꼬임(장력) 확보<br>3. <b>에너지 전이:</b> 메디신볼 오버헤드 스로우로 상하체 폭발 타이밍 교정", 
        "c_throw_kids": "<b>[🎯 미션: 거대한 고무줄 새총!]</b><br>멀리 던지려면 팔 힘만 쓰면 안 돼요! 몸 전체를 팽팽한 고무줄 새총처럼 만들어야 해요.<br><br><b>1단계:</b> 던지기 직전 앞발을 땅에 디디면서 '얼음!' 하고 앞무릎을 빳빳하게 세우세요.<br><b>2단계:</b> 하체는 멈춰있고, 뒤로 젖혀진 상체와 팔만 고무줄이 튕겨 나가듯 '휙!' 던지세요.<br><b>3단계:</b> 젖은 수건을 털어내듯 마지막에 손끝을 강하게 채주면 완벽해요!", 
        
        # [경보 텍스트 보강]
        "c_walk_pro": "<b>[역학 진단: Straight Leg Rule 위반]</b><br>경보의 핵심인 앞다리 완전 신전 규정을 위반하여 <span style='color:#D93025; font-weight:bold;'>{avg_angle}°</span>로 측정되었습니다. 공식 대회 실격(Red Card) 사유이며, 골반 롤링 대신 무릎을 사용하여 추진력을 얻고 있습니다.<br><br><b>[교정 프로토콜]</b><br>1. <b>락킹 훈련:</b> 발뒤꿈치가 지면에 닿는 순간부터 수직을 지날 때까지 무릎 관절 100% 고정<br>2. <b>골반 롤링:</b> 좁아진 보폭을 극복하기 위한 골반의 전후 수평 회전(Pelvic Rotation) 극대화<br>3. <b>암 크로스:</b> 골반 회전을 상쇄하기 위한 코어 밸런스 유지 및 크로스 암 스윙", 
        "c_walk_kids": "<b>[🚶‍♂️ 미션: 무릎 펴고 모델 걷기!]</b><br>경보에서는 무릎이 구부러지면 반칙이에요! 다리를 젓가락처럼 일자로 쫙 펴야 해요.<br><br><b>1단계:</b> 앞발이 땅에 닿을 때 무릎이 절대 굽혀지지 않게 다리 뒷근육을 팽팽하게 만드세요.<br><b>2단계:</b> 다리가 안 굽혀져서 걷기 힘들면 엉덩이(골반)를 씰룩쌜룩 크게 흔들어서 앞으로 나가세요.<br><b>3단계:</b> 팔은 가슴 앞쪽으로 힘차게 흔들며 패션 모델처럼 당당하게 걸어보세요!"
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

benchmark_db = {
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica Elite": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 US Elite": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}, "🇰🇷 Korea Elite": {"angle": 167.5, "radar": [88, 90, 82, 88, 90], "color": "#CD2E3A"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya Elite": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}, "🇯🇵 Japan Elite": {"angle": 163.5, "radar": [87, 89, 82, 87, 91], "color": "#BC002D"}, "🇰🇷 Korea Elite": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China Elite": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}, "🇪🇸 Spain Elite": {"angle": 178.8, "radar": [96, 92, 95, 96, 94], "color": "#F1BF00"}, "🇰🇷 Korea Elite": {"angle": 178.5, "radar": [95, 90, 92, 94, 90], "color": "#CD2E3A"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇨🇺 Cuba Elite": {"angle": 177.5, "radar": [96, 94, 98, 93, 94], "color": "#CB1515"}, "🇺🇸 US Elite": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}, "🇰🇷 Korea Elite": {"angle": 170.0, "radar": [85, 88, 82, 85, 88], "color": "#CD2E3A"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇩🇪 Germany Elite": {"angle": 174.5, "radar": [96, 98, 97, 95, 96], "color": "#FFCE00"}, "🇨🇿 Czech Elite": {"angle": 173.0, "radar": [95, 97, 95, 94, 95], "color": "#11457E"}, "🇰🇷 Korea Elite": {"angle": 168.0, "radar": [85, 88, 86, 85, 87], "color": "#CD2E3A"}}
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
    selected_lang = "🇰🇷 한국어"
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

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.4em; color:#64FFDA;'>🌍 {t['title']}</h1>
        <p style='margin:5px 0 0 0; color:#CCD6F6;'>{t['sub']}</p></div>
        <div><span style="background: rgba(100,255,218,0.1); color: #64FFDA; padding: 10px 25px; border-radius: 30px; font-weight: 800; border: 1px solid rgba(100,255,218,0.3);">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 딥러닝 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('Deep Learning Analysis & Coaching Protocol Generating...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        
        if b_group_name == "Sprint": avg_angle = 158.5
        elif b_group_name == "Distance": avg_angle = 155.9
        elif b_group_name == "Walk": avg_angle = 172.0
        elif b_group_name == "Jump": avg_angle = 162.5
        elif b_group_name == "Throw": avg_angle = 158.0
        
        target_angle = b_data['angle']; gap = target_angle - avg_angle
        bench_name = selected_bench.split(" ")[0]; current_metrics = categories[selected_cat]["metrics"]
        
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
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'family': "Pretendard"})
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin: 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), name='고정축'))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8), name=f'내 궤적 ({avg_angle}°)'))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'표준 ({target_angle}°)'))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=550, showlegend=True)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        
        if b_group_name == "Sprint":
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: st.markdown(t['c_mara_pro'].format(gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        elif b_group_name == "Walk":
            with tab_pro: st.markdown(t['c_walk_pro'].format(avg_angle=avg_angle), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_walk_kids'], unsafe_allow_html=True)
        elif b_group_name == "Jump":
            with tab_pro: st.markdown(t['c_jump_pro'].format(avg_angle=avg_angle), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_jump_kids'], unsafe_allow_html=True)
        elif b_group_name == "Throw":
            with tab_pro: st.markdown(t['c_throw_pro'].format(gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_throw_kids'], unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown(f"""<div class="vision-card"><h3 style="color: #1A73E8;">{t['vision_title']}</h3><p>{t['vision_desc']}</p></div>""", unsafe_allow_html=True)

# 8. 구글 엑셀 연동
st.markdown("---")
with st.form(key='athletics_ai_form', clear_on_submit=True):
    user_comment = st.text_area(t['f_title'], placeholder=t['f_desc'])
    submit_button = st.form_submit_button(label="의견 전송", type="primary")
    if submit_button and user_comment:
        try:
            url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
            data = {"entry.503694872": user_comment}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data)
            urllib.request.urlopen(req)
            st.balloons(); st.success(t['f_success'])
        except: st.error("전송 오류")
