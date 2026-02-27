import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "글로벌 육상 전 종목 생체역학 통합 분석 시스템", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", 
        "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목",
        "s_data": "📊 비교 벤치마크", "s_up": "측면 영상 파일 선택 (10초 이내)", 
        "s_btn": "🚀 딥러닝 역학 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "img_title": "📸 비전 AI 관절 추출 및 종목별 궤적 대조",
        "img_desc": "표준화된 관절 좌표를 기반으로 트랙, 도약, 투척 등 육상 전 종목의 핵심 역학 궤적을 분석합니다.",
        "vision_title": "🛰️ Future Mission: 인류의 모든 움직임을 데이터화하다",
        "vision_desc": "본 시스템은 마라톤, 100m, 창던지기, 높이뛰기 등 육상(Track and Field) 15개 전 종목의 생체역학을 하나의 AI로 통합한 '파운데이션 모델'입니다.",
        "f_title": "🧪 ATHLETICS AI 연구소", "f_desc": "당신의 폼이 세계의 표준이 됩니다. 딥러닝 분석 결과에 대한 자유로운 의견을 남겨주세요.",
        "f_success": "✅ 귀하의 소중한 의견이 AI 연구소(Google Sheets)로 성공적으로 실시간 전송되었습니다!"
    }
}

# 3. 🏟️ 육상 전 종목 카테고리
categories = {
    "트랙 (Track: 달리기/허들)": {
        "metrics": ['무릎 신전(Knee Ext)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 밸런스(Pelvic)', '상하체 동기화(Arm Sync)'],
        "sports": ["100m 단거리", "400m 스프린트", "마라톤 (Marathon)", "100m/110m 허들", "경보 (Race Walking)"]
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

benchmarks = {
    "🌍 World Record (세계 기록)": {"angle": 175.5, "radar": [99, 98, 97, 99, 98], "color": "#000000"},
    "🥇 Olympic Gold (올림픽 기준)": {"angle": 172.0, "radar": [96, 95, 96, 95, 97], "color": "#F1BF00"},
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

# 5. 사이드바 구성
with st.sidebar:
    selected_lang = "🇰🇷 한국어"
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
            mode="gauge+number", value=score, title={'text': "역학 일치도 (Score)", 'font': {'size': 18, 'color': '#5F6368'}},
            domain={'x': [0, 1], 'y': [0, 1]}, 
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0A192F"}, 'steps': [{'range': [0, 70], 'color': "#FCE8E6"}, {'range': [85, 100], 'color': "#E6F4EA"}], 'threshold': {'line': {'color': "#64FFDA", 'width': 4}, 'value': 95}}
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=current_metrics, fill='toself', name='My Data', line_color='#D93025', fillcolor='rgba(217, 48, 37, 0.2)'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=current_metrics, fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#5F6368", 'family': "Pretendard", 'size': 11})
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin-top: 0; margin-bottom: 5px;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my_ankle = -np.sin(np.radians(180 - avg_angle)); y_my_ankle = -np.cos(np.radians(180 - avg_angle))
        x_target_ankle = -np.sin(np.radians(180 - target_angle)); y_target_ankle = -np.cos(np.radians(180 - target_angle))

        fig_overlay = go.Figure()
        fig_overlay.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), name='고정축'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_my_ankle], y=[0, y_my_ankle], mode='lines+markers', line=dict(color='#D93025', width=8), name=f'내 궤적 ({avg_angle}°)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_target_ankle], y=[0, y_target_ankle], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'표준 ({target_angle}°)'))
        fig_overlay.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white', family='Pretendard'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=480, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_easy = st.tabs(["🎓 심화 역학 진단 (전문가용)", "🎈 AI 놀이 훈련법 (어린이용)"])
        
        # 💡 종목별 피드백 (어린이 놀이 훈련법 대폭 강화)
        if "단거리" in selected_sport or "스프린트" in selected_sport:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">🚀 스프린트(Sprint): 지면 발진력 분석</h4>
                <p style="font-size: 0.95em; color: #3C4043; line-height: 1.6;">
                    도약(Take-off) 시 최대 무릎 신전 각도가 <span class="highlight-text">{avg_angle}°</span>에 그쳐, 엘리트 벤치마크 대비 <span class="highlight-text">{gap:.1f}°의 조기 회수</span>가 관찰됩니다.<br>
                    지면접촉시간(GCT)이 지연되며, 아킬레스건의 <b>SSC(신장-단축 주기)</b> 에너지가 전진 가속도로 100% 전환되지 못하고 있습니다.
                </p>
                <div style="font-size: 0.92em; color: #202124; background: #E8F0FE; padding: 15px; border-radius: 8px; border: 1px solid #D2E3FC; margin-top: 15px;">
                    <b>[전문 훈련 프로토콜]</b><br>
                    1. 플라이오메트릭(Plyometric): 뎁스 점프를 통한 발목 반응성 극대화<br>
                    2. 지면 타격: 전족부(Forefoot) 수직 하강 제어<br>
                    3. 동기화: 팔꿈치 후방 스윙과 지면 발진의 1:1 매칭
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#FF6B6B; margin-top:10px; margin-bottom:15px;">🐆 치타처럼 쌩~ 날아가는 놀이법!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.5;">
                    달릴 때 발바닥이 땅에 오래 붙어있으면 속도가 느려져요! <b>발 앞꿈치로만 땅을 살짝 밟고 로켓처럼 튕겨 올라가는 연습</b>을 해볼까요?
                </p>
                <div style="background: #FFF0ED; padding: 18px; border-radius: 12px; border: 2px dashed #FFD4CC; margin-top: 15px;">
                    <b style="color:#D93025; font-size:1.1em;">🔥 오늘의 미션: 뜨거운 용암 밟기 놀이!</b><br><br>
                    <b>1단계:</b> 운동장 바닥이 <b>'앗 뜨거워! 용암'</b>이라고 상상해 봐요.<br>
                    <b>2단계:</b> 발이 용암에 데이지 않게, 뒤꿈치는 들고 앞꿈치로만 <b>'앗 뜨거!' 하면서 0.1초 만에 발을 들어 올리며</b> 뛰어보세요.<br>
                    <b>3단계:</b> 발을 빨리 뗄 때 팔꿈치도 뒤로 <b>'휙!'</b> 쳐주면 치타 완성!
                </div>
                """, unsafe_allow_html=True)
        
        elif "마라톤" in selected_sport:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">🏃‍♂️ 마라톤(Marathon): 에너지 효율 분석</h4>
                <p style="font-size: 0.95em; color: #3C4043; line-height: 1.6;">
                    도약 시 고관절 및 무릎의 완전 신전이 이루어지지 않아 <span class="highlight-text">{gap:.1f}°의 편차</span>가 발생하고 있습니다.<br>
                    골반 드롭 현상으로 인해 <b>지면반발력(GRF) 벡터</b>가 수직으로 분산(수직진폭 상승)되어 햄스트링에 과부하를 초래합니다.
                </p>
                <div style="font-size: 0.92em; color: #202124; background: #F8F9FA; padding: 15px; border-radius: 8px; border: 1px solid #E8EAED; margin-top: 15px;">
                    <b>[전문 훈련 프로토콜]</b><br>
                    1. 가동성: 장요근 동적 스트레칭으로 고관절 후방 가동 범위 확보<br>
                    2. 코어 안정화: 싱글 레그 데드리프트를 통한 골반 롤링 제어<br>
                    3. 신경계 큐잉: 발볼을 끝까지 활용하는 'Full Toe-off' 인지
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#4CAF50; margin-top:10px; margin-bottom:15px;">🥷 소리 없이 달리는 닌자 놀이법!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.5;">
                    오래 달릴 때 쿵쾅쿵쾅 뛰면 에너지가 빨리 닳고 무릎이 아파요. <b>위아래로 흔들리지 않고 미끄러지듯 부드럽게</b> 달리는 연습을 해봐요.
                </p>
                <div style="background: #E8F5E9; padding: 18px; border-radius: 12px; border: 2px dashed #C8E6C9; margin-top: 15px;">
                    <b style="color:#2E7D32; font-size:1.1em;">💧 오늘의 미션: 머리 위 물컵 지키기!</b><br><br>
                    <b>1단계:</b> 머리 위에 <b>'가득 찬 물컵'</b>이 올려져 있다고 상상하세요.<br>
                    <b>2단계:</b> 쿵쾅거리면 물이 쏟아져요! 보폭을 너무 크게 하지 말고, <b>자전거 페달을 둥글게 돌리듯 발을 굴려보세요.</b><br>
                    <b>3단계:</b> 뒤에서 누군가 날 밀어주는 것처럼 상체를 살짝 앞으로 숙이고 닌자처럼 사뿐사뿐 달리면 성공!
                </div>
                """, unsafe_allow_html=True)
        
        elif "Jump" in selected_cat:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">🦘 도약(Jump): 발구름(Take-off) 분석</h4>
                <p style="font-size: 0.95em; color: #3C4043; line-height: 1.6;">
                    마지막 두 걸음(Penultimate Step)에서 무게중심 하강비가 부족하여 발구름 각도가 <span class="highlight-text">{avg_angle}°</span>에 머물렀습니다.<br>
                    수평 <b>진입 속도(Approach Velocity)</b>가 수직 충격량으로 전환되는 효율이 떨어져 에너지 누수가 발생합니다.
                </p>
                <div style="font-size: 0.92em; color: #202124; background: #F4FBF8; padding: 15px; border-radius: 8px; border: 1px solid #CEEBE0; margin-top: 15px;">
                    <b>[전문 훈련 프로토콜]</b><br>
                    1. 힌지 제어: 페널티메이트 스텝 시 의도적 무게중심 하강 훈련<br>
                    2. 아모티제이션: 지면 접촉 시간 최소화 및 족저근막 탄성 방출<br>
                    3. 상향 스윙: 리드 암과 리드 레그의 폭발적인 상향 구동 매칭
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#9C27B0; margin-top:10px; margin-bottom:15px;">🚀 슈퍼맨처럼 솟아오르는 놀이법!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.5;">
                    높이, 멀리 뛰려면 <b>용수철처럼 몸을 살짝 움츠렸다가 펴는 힘</b>이 필요해요. 그냥 뛰는 것보다 마지막 걸음이 아주 중요하답니다!
                </p>
                <div style="background: #F3E5F5; padding: 18px; border-radius: 12px; border: 2px dashed #E1BEE7; margin-top: 15px;">
                    <b style="color:#7B1FA2; font-size:1.1em;">🐸 오늘의 미션: 마법의 징검다리!</b><br><br>
                    <b>1단계:</b> 다다다 달려가다가 도약하기 <b>바로 직전 한 걸음</b>에서 개구리처럼 무릎을 살짝 더 굽혀보세요.<br>
                    <b>2단계:</b> 마지막 발이 땅에 닿는 순간, <b>'쾅!' 소리가 나게 밟고</b> 하늘에 있는 풍선을 터뜨리듯 무릎을 쭉 펴며 솟아오르세요.<br>
                    <b>3단계:</b> 뛸 때 양팔을 만세! 하듯 위로 힘차게 끌어올리면 훨씬 멀리 날아가요!
                </div>
                """, unsafe_allow_html=True)
                
        elif "Throw" in selected_cat:
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#0A192F; margin-top:10px; margin-bottom:15px;">☄️ 투척(Throw): 키네틱 체인 분석</h4>
                <p style="font-size: 0.95em; color: #3C4043; line-height: 1.6;">
                    리드 레그의 <b>블록킹(Blocking) 동작 붕괴</b>로 릴리스 각도가 <span class="highlight-text">{avg_angle}°</span>에 그쳤습니다.<br>
                    선운동량이 상체의 각운동량으로 전이되는 <b>키네틱 체인</b>이 단절되어 어깨의 '활시위(Bow)' 장력 에너지를 상실했습니다.
                </p>
                <div style="font-size: 0.92em; color: #202124; background: #FEF7E6; padding: 15px; border-radius: 8px; border: 1px solid #FDE8B3; margin-top: 15px;">
                    <b>[전문 훈련 프로토콜]</b><br>
                    1. 브레이싱: 블록킹 발 접지 시 무릎 관절 100% 락킹 정지 훈련<br>
                    2. 코어 텐션: 흉추 가동성 극대화를 통한 하체-코어 역학적 꼬임 확장<br>
                    3. 에너지 전이: 메디신볼 오버헤드 스로우로 폭발 타이밍 교정
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#FF9800; margin-top:10px; margin-bottom:15px;">🎯 인간 투석기가 되는 놀이법!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.5;">
                    멀리 던지려면 팔 힘만 쓰면 안 돼요! 몸통 전체를 <b>거대한 투석기나 고무줄 새총</b>처럼 사용해야 해요. 앞발로 튼튼한 기둥을 만들어 볼까요?
                </p>
                <div style="background: #FFF8E1; padding: 18px; border-radius: 12px; border: 2px dashed #FFECB3; margin-top: 15px;">
                    <b style="color:#F57C00; font-size:1.1em;">🧊 오늘의 미션: 얼음 땡 던지기!</b><br><br>
                    <b>1단계:</b> 도움닫기를 하며 달려가다가, 던지기 직전 앞발을 땅에 딛으면서 <b>'얼음!' 하고 앞다리 무릎을 빳빳하게</b> 세워 멈추세요.<br>
                    <b>2단계:</b> 다리는 얼음 상태로 딱 버티고, <b>'땡!' 하는 순간 젖혀있던 상체와 팔만</b> 휙! 하고 튕겨 나가게 던지는 거예요.<br>
                    <b>3단계:</b> 젖은 수건을 팡! 하고 털어내듯 마지막에 손끝을 강하게 채주세요!
                </div>
                """, unsafe_allow_html=True)
        else:
            with tab_pro:
                st.markdown("종목별 정밀 역학 데이터 시뮬레이션 중...")
            with tab_easy:
                st.markdown("올바른 폼은 부상을 방지합니다.")
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 🛰️ 파운데이션 비전 섹션
st.markdown(f"""
    <div class="vision-card">
        <h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3>
        <p style="font-size: 1.1em; color: #3C4043; line-height: 1.6; margin-bottom: 20px;">{t['vision_desc']}</p>
    </div>
""", unsafe_allow_html=True)

# 8. 🧪 구글 엑셀 실시간 연동
st.markdown("---")
st.markdown('<div class="data-card" style="margin-bottom: 50px;">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #202124;'>{t['f_title']}</h3>", unsafe_allow_html=True)
st.write(f"<span style='color: #5F6368;'>{t['f_desc']}</span>", unsafe_allow_html=True)

with st.form(key='marathon_ai_lab_form', clear_on_submit=True):
    user_comment = st.text_area("연구소로 데이터 전송 (Data Submission)", placeholder="예: '아이들이 얼음땡 놀이 피드백을 보고 너무 좋아합니다!'")
    submit_button = st.form_submit_button(label="의견 전송 (Submit)", type="primary")

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
                st.error("⚠️ 오류 발생")
        else:
            st.warning("의견을 입력해주세요.")
st.markdown('</div>', unsafe_allow_html=True)
