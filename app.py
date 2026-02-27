import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정 (레이아웃을 가장 넓게)
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (전문가 & 어린이 코칭 텍스트 압도적 보강)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", 
        "sub": "인류의 모든 움직임을 데이터화하는 글로벌 육상 생체역학 통합 파운데이션", 
        "s_head": "⚙️ 시스템 설정", "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 벤치마크 (국가별 최상위)", "s_up": "측면 영상 업로드 (10초 이내)", "s_btn": "🚀 AI 딥 코칭 실행", "r_title": "🔬 AI 생체역학 정밀 진단 리포트",
        
        # [단거리 100m 코칭]
        "c_sprint_pro": """
            <span style='color:#1A73E8; font-weight:800; font-size:1.1em;'>🎯 [강점 분석 및 칭찬]</span><br>
            높은 케이던스 유지 능력과 상체 전방 기울기는 세계적인 스플린터들의 초기 가속 패턴과 일치하는 훌륭한 강점입니다.<br><br>
            <span style='color:#D93025; font-weight:800; font-size:1.1em;'>🚨 [약점 및 역학 진단]</span><br>
            하지만 도약(Take-off) 시 무릎 신전 각도가 <b>{avg_angle}°</b>에 그쳐, 엘리트 기준({target_angle}°) 대비 <b>{gap:.1f}°의 조기 회수(Early Recovery)</b>가 관찰됩니다. 이는 발목 배측굴곡이 무너지며 아킬레스건의 SSC(신장-단축 주기) 탄성 에너지가 전진 가속도로 100% 전환되지 못하고 지면으로 흩어지는 '힘의 누수'를 발생시킵니다.<br><br>
            <span style='color:#0F9D58; font-weight:800; font-size:1.1em;'>💡 [단계별 문제 해결 프로토콜]</span><br>
            1. <b>플라이오메트릭 훈련:</b> 뎁스 점프(Depth Jump)를 통해 발목과 건의 반응 강성(Stiffness)을 극대화하여 지면 접촉 시간(GCT)을 최소화하십시오.<br>
            2. <b>지면 타격 제어:</b> A-Skip 수행 시, 발바닥 전체가 아닌 '전족부(Forefoot)'로 수직 하강 타격하는 리듬을 뇌에 각인시키세요.<br>
            3. <b>상하체 역학 동기화:</b> 지면 발진과 동시에 반대쪽 팔꿈치를 뒤로 가장 강하고 짧게 끊어 치는 훈련을 주 3회 병행하십시오.
        """, 
        "c_sprint_kids": """
            <span style='color:#FF6B6B; font-weight:800; font-size:1.1em;'>🌟 [AI 코치님의 칭찬]</span><br>
            우리 친구, 달릴 때 팔을 씩씩하게 흔들고 앞을 쳐다보는 눈빛이 정말 멋져요! 이대로 조금만 다듬으면 우사인 볼트보다 빠른 로켓이 될 수 있겠는걸요?<br><br>
            <span style='color:#FF9800; font-weight:800; font-size:1.1em;'>🔥 [오늘의 상상력 놀이: 뜨거운 용암 밟기]</span><br>
            발바닥 전체가 땅에 '쿵쾅' 닿으면 속도가 줄어들어요! 바닥이 아주 뜨거운 용암이라고 상상해 봐요.<br>
            <b>1단계:</b> 뒤꿈치를 살짝 들고 앞꿈치로만 '앗 뜨거!' 하면서 0.1초 만에 발을 떼세요.<br>
            <b>2단계:</b> 발을 뗄 때 팔꿈치를 뒤로 휙! 치면 치타처럼 몸이 튕겨 나가요.<br>
            <b>3단계:</b> 땅을 가볍게, 하지만 세게 밟을수록 몸이 붕~ 날아가는 느낌을 즐겨보세요!<br><br>
            <span style='color:#4CAF50; font-weight:800; font-size:1.1em;'>👨‍🏫 [부모님 및 지도자를 위한 가이드]</span><br>
            아이가 달릴 때 뒤꿈치가 먼저 땅에 닿는지(힐 스트라이크) 확인해 주세요. 바닥에 일정한 간격으로 선을 그어주고, 선과 선 사이를 '앞꿈치'로만 통통 튕기며 지나가도록 리듬감을 심어주는 것이 가장 효과적입니다.
        """,
        
        # [마라톤 코칭]
        "c_mara_pro": """
            <span style='color:#1A73E8; font-weight:800; font-size:1.1em;'>🎯 [강점 분석 및 칭찬]</span><br>
            착지 시 상하체의 흔들림이 적고 일정한 호흡 리듬을 유지하는 것은 장거리 러닝의 훌륭한 기본기를 갖추고 있다는 증거입니다.<br><br>
            <span style='color:#D93025; font-weight:800; font-size:1.1em;'>🚨 [약점 및 역학 진단]</span><br>
            도약 시 고관절과 무릎의 완전 신전(Triple Extension)이 이루어지지 않아 <b>{gap:.1f}°의 편차</b>가 발생합니다. 이로 인해 지면반발력(GRF)이 전진하는 수평 에너지가 아닌, 수직(위아래)으로 분산되어 에너지 누수가 극심해집니다. 장거리 러닝 시 무릎 관절과 햄스트링에 불필요한 과부하를 초래합니다.<br><br>
            <span style='color:#0F9D58; font-weight:800; font-size:1.1em;'>💡 [단계별 문제 해결 프로토콜]</span><br>
            1. <b>가동성 확장:</b> 장요근 및 고관절 굴곡근 동적 스트레칭을 통해 후방 신전 가동 범위를 물리적으로 넓히세요.<br>
            2. <b>코어 및 골반 안정화:</b> 싱글 레그 데드리프트(Unilateral)를 통해 중둔근 밸런스를 잡고 골반 드롭(Pelvic Drop)을 억제하십시오.<br>
            3. <b>미드풋 스트라이크:</b> 발을 몸의 무게중심(COM) 바로 아래에 디뎌 브레이킹 포스를 최소화하고 자연스럽게 굴러가듯 달려야 합니다.
        """, 
        "c_mara_kids": """
            <span style='color:#FF6B6B; font-weight:800; font-size:1.1em;'>🌟 [AI 코치님의 칭찬]</span><br>
            포기하지 않고 끝까지 일정한 속도로 달리는 모습이 대단해요! 진정한 마라토너의 끈기를 가졌네요.<br><br>
            <span style='color:#4CAF50; font-weight:800; font-size:1.1em;'>💧 [오늘의 상상력 놀이: 닌자의 물컵 지키기]</span><br>
            위아래로 쿵쾅쿵쾅 뛰면 에너지가 빨리 닳고 무릎이 아파요. 머리 위에 가득 찬 물컵이 있다고 상상해 볼까요?<br>
            <b>1단계:</b> 점프하듯 뛰지 말고, 자전거 페달을 부드럽게 돌리듯 발을 둥글게 굴려보세요.<br>
            <b>2단계:</b> 뒤에서 보이지 않는 바람이 날 밀어준다고 생각하고 상체를 살짝만 앞으로 기울이세요.<br>
            <b>3단계:</b> 발소리가 나지 않게 사뿐사뿐 닌자처럼 달리면 물을 한 방울도 안 흘릴 수 있어요!<br><br>
            <span style='color:#FF9800; font-weight:800; font-size:1.1em;'>👨‍🏫 [부모님 및 지도자를 위한 가이드]</span><br>
            아이의 달리기 소리가 유난히 크다면, 수직 진폭이 너무 크다는 뜻입니다. "보폭을 넓혀라"라고 지시하기보다 "머리가 천장에 닿지 않게 스르륵 달려보자"고 큐잉(Cueing)을 주어 부드러운 폼을 유도해 주세요.
        """,
        
        # [경보/도약/투척 등은 공간상 범용 코칭으로 통합 - 15개 종목을 커버하는 핵심 텍스트]
        "c_general_pro": """
            <span style='color:#1A73E8; font-weight:800; font-size:1.1em;'>🎯 [역학적 강점]</span><br>
            해당 종목의 필수적인 기본 자세와 밸런스 유지 능력이 매우 우수합니다.<br><br>
            <span style='color:#D93025; font-weight:800; font-size:1.1em;'>🚨 [역학 진단 및 에너지 누수]</span><br>
            핵심 관절 각도 측정 결과 <b>{avg_angle}°</b>로, 세계 표준({target_angle}°) 대비 <b>{gap:.1f}°의 편차</b>를 보입니다. 이는 운동 사슬(Kinetic Chain)의 연결을 약화시켜, 하체에서 발생한 에너지가 최종 퍼포먼스로 100% 전환되지 못하는 원인이 됩니다.<br><br>
            <span style='color:#0F9D58; font-weight:800; font-size:1.1em;'>💡 [문제 해결 프로토콜]</span><br>
            1. <b>가동성 및 강성 훈련:</b> 해당 관절의 가동 범위를 늘리거나(스트레칭), 버티는 힘(브레이싱)을 기르는 기초 공사가 필요합니다.<br>
            2. <b>무게중심(COM) 제어:</b> 힘을 써야 할 순간(발구름, 릴리스 등) 직전에 무게중심을 낮추어 폭발력을 장전하는 훈련을 반복하십시오.<br>
            3. <b>상하체 협응:</b> 하체의 힘이 낭비되지 않도록 팔스윙과 상체 비틀림을 정확한 타이밍에 동기화(Sync)해야 합니다.
        """,
        "c_general_kids": """
            <span style='color:#FF6B6B; font-weight:800; font-size:1.1em;'>🌟 [AI 코치님의 칭찬]</span><br>
            자신감 넘치게 훈련하는 모습이 금메달감이에요! 운동을 즐기는 자세가 가장 큰 재능이랍니다.<br><br>
            <span style='color:#9C27B0; font-weight:800; font-size:1.1em;'>🚀 [오늘의 상상력 놀이: 슈퍼 히어로 변신!]</span><br>
            관절을 덜 쓰면 힘이 중간에 사라져요! 몸을 커다란 용수철이나 투석기라고 상상해 볼까요?<br>
            <b>1단계:</b> 에너지를 모으기 위해 힘을 쓰기 직전에 몸을 살짝 더 움츠리거나 앞발로 꽉 버텨보세요 (얼음!).<br>
            <b>2단계:</b> 쌓인 에너지를 1초 만에 폭발시키며 '땡!' 하고 힘을 쏟아내세요.<br>
            <b>3단계:</b> 팔을 하늘로 뻗거나 뒤로 강하게 쳐주면 슈퍼 히어로처럼 훨씬 멀리, 높이, 빠르게 갈 수 있어요!<br><br>
            <span style='color:#4CAF50; font-weight:800; font-size:1.1em;'>👨‍🏫 [부모님 및 지도자를 위한 가이드]</span><br>
            아이들에게 "각도를 굽혀라, 펴라"는 기계적인 지시보다, "스프링처럼 튕겨봐", "고무줄처럼 늘려봐" 같은 비유적 표현(Metaphor)을 사용하세요. 아이가 스스로 리듬과 타이밍을 찾도록 칭찬으로 이끌어주는 것이 핵심입니다.
        """
    }
}

# 3. 🏟️ 육상 전 종목 카테고리 (유지)
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
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica Elite": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 US Elite": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya Elite": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}, "🇰🇷 Korea Elite": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China Elite": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 US Elite": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇩🇪 Germany Elite": {"angle": 174.5, "radar": [96, 98, 97, 95, 96], "color": "#FFCE00"}}
}

# 4. 고급 CSS (중앙 정렬 타이틀 지원)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    
    /* 전면 배치된 Hero Section 타이틀 */
    .hero-section {
        background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%);
        padding: 50px 20px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .hero-title {
        color: #64FFDA;
        font-size: 3.5em;
        font-weight: 900;
        letter-spacing: 2px;
        margin: 0 0 10px 0;
        text-shadow: 0px 4px 15px rgba(100, 255, 218, 0.3);
    }
    .hero-sub {
        color: #CCD6F6;
        font-size: 1.2em;
        font-weight: 400;
        margin: 0;
    }
    
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 구성 
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

# 🚀 첫 화면 전면 배치 (Hero Section)
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t['title']}</h1>
        <p class="hero-sub">{t['sub']}</p>
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

    # 하단 2단 레이아웃 (오버레이 vs 코칭 박스)
    col3, col4 = st.columns([1, 1.3])
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
        
        # 종목별로 심화된 코칭 텍스트 출력
        if b_group_name == "Sprint":
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: st.markdown(t['c_mara_pro'].format(gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        else: # 그 외 종목 통합 코칭
            with tab_pro: st.markdown(t['c_general_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_general_kids'], unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px;">
        <h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3><p style="font-size: 1.1em; color: #3C4043;">{t['vision_desc']}</p>
    </div>
""", unsafe_allow_html=True)

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
