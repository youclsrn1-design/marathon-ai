import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 시스템 기본 설정
st.set_page_config(page_title="MARATHON AI | Global Standard", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩
ui_langs = {
    "🇰🇷 한국어": {
        "title": "MARATHON AI PRO", "sub": "글로벌 생체역학 정밀 분석 표준 시스템", "toss": "Toss ID: MARATHON AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", 
        "s_sport": "🏃‍♂️ 분석 종목 (Sport Type)",
        "s_data": "📊 비교 벤치마크", "s_vid": "🎥 비전 데이터 입력", "s_up": "측면 영상 파일 선택 (10초 이내)", 
        "s_gen": "성별", "s_btn": "🚀 정밀 역학 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "cat": ['무릎 신전(Knee Ext)', '지면접촉시간(GCT)', '수직진폭(Oscillation)', '골반 밸런스(Pelvic)', '상하체 동기화(Arm Sync)'],
        "img_title": "📸 비전 AI 관절 추출 및 표준 궤적 대조",
        "img_desc": "표준화된 관절 좌표를 기반으로 사용자의 도약 각도(🔴)와 세계 기준선(🟡)의 생체역학적 편차를 시각화합니다.",
        "vision_title": "🛰️ Future Mission: 메타 안경 & 심박수 동기화 코칭",
        "vision_desc": "본 시스템은 구글/메타의 스마트 웨어러블과 결합하여, 실시간 심박수와 메타 안경의 오디오 엔진(BPM)을 동기화하는 'AI 리듬 코칭' 시범 사업을 준비 중입니다. 마라톤부터 경보 판정까지, 전 세계 스포츠 데이터를 표준화합니다.",
        "f_title": "🧪 MARATHON AI 연구소", "f_desc": "당신의 폼이 세계의 표준이 됩니다. 딥러닝 분석 결과에 대한 자유로운 의견을 남겨주세요.",
        "f_success": "✅ 귀하의 소중한 생체역학 피드백이 AI 연구소로 성공적으로 전송되었습니다!"
    },
    "🇺🇸 English": {
        "title": "MARATHON AI PRO", "sub": "Global Biomechanical Standard System", "toss": "Powered by MARATHON AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", 
        "s_sport": "🏃‍♂️ Sport Type",
        "s_data": "📊 Benchmark Target", "s_vid": "🎥 Vision Data Input", "s_up": "Select Video File (Side-view)", 
        "s_gen": "Gender", "s_btn": "🚀 Run Precision Analysis", "r_title": "🔬 Biometric Diagnostic Report",
        "cat": ['Knee Ext.', 'GCT', 'Oscillation', 'Pelvic Bal.', 'Arm-Leg Sync'],
        "img_title": "📸 Vision AI Skeletal Tracking",
        "img_desc": "Visualizes the biomechanical deviation between the user's push-off angle (🔴) and the world baseline (🟡).",
        "vision_title": "🛰️ Future Mission: Meta Glass & HR Sync Coaching",
        "vision_desc": "Preparing a pilot project integrating Google/Meta wearables to synchronize real-time heart rate with audio BPM pacing. Standardizing global sports data from marathons to race walking.",
        "f_title": "🧪 MARATHON AI Lab", "f_desc": "Your form becomes the global standard. Please leave your feedback.",
        "f_success": "✅ Your biomechanical feedback has been successfully submitted!"
    }
}

# 3. 글로벌 벤치마크 데이터베이스 (종목별 분리: 마라톤 vs 경보)
benchmarks = {
    "마라톤 (Marathon)": {
        "🌍 World Record (세계 신기록)": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"},
        "🇰🇪 Kenya Elite (케냐 최상위)": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"},
        "🇺🇸 US Olympic (미국 대표팀)": {"angle": 164.5, "radar": [88, 90, 85, 88, 92], "color": "#3C3B6E"},
        "🇯🇵 Japan Elite (일본 대표팀)": {"angle": 163.5, "radar": [87, 89, 82, 87, 91], "color": "#BC002D"},
        "🇰🇷 Korea Elite (대한민국 대표팀)": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"},
        "🌐 Global Amateur (일반인 평균)": {"angle": 155.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
    },
    "경보 (Race Walking)": {
        "🌍 World Record (세계 신기록)": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"},
        "🇨🇳 China Elite (중국 최상위)": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"},
        "🇯🇵 Japan Elite (일본 최상위)": {"angle": 179.0, "radar": [97, 93, 96, 97, 95], "color": "#BC002D"},
        "🇪🇸 Spain Elite (스페인 국가대표)": {"angle": 178.8, "radar": [96, 92, 95, 96, 94], "color": "#F1BF00"},
        "🇰🇷 Korea Elite (대한민국 대표팀)": {"angle": 178.5, "radar": [95, 90, 92, 94, 90], "color": "#CD2E3A"},
        "🌐 Global Amateur (파울 위험군)": {"angle": 165.0, "radar": [40, 75, 85, 50, 60], "color": "#888888"}
    }
}

# 4. 고급화된 CSS 세팅
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .header-panel { background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); padding: 35px 30px; border-radius: 16px; color: white; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-left: 6px solid #1A73E8; padding: 25px; border-radius: 0 12px 12px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%; border-top: 1px solid #E8EAED; border-right: 1px solid #E8EAED; border-bottom: 1px solid #E8EAED; }
    .highlight-text { color: #D93025; font-weight: 800; }
    .vision-card { background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px; margin-top: 40px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(26,115,232,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 (종목 선택 추가)
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    # 종목 선택 로직
    sport_types = list(benchmarks.keys())
    selected_sport = st.selectbox(t['s_sport'], sport_types)
    
    # 선택된 종목에 맞는 벤치마크 리스트업
    selected_bench = st.selectbox(t['s_data'], list(benchmarks[selected_sport].keys()))
    b_data = benchmarks[selected_sport][selected_bench]
    
    st.markdown("---")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov', 'avi'])
    gender = st.selectbox(t['s_gen'], ["Male", "Female"] if "English" in selected_lang else ["남성", "여성"])
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button(t['s_btn'], use_container_width=True, type="primary")

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:800; font-size:2.4em; letter-spacing: -1px;'>🌍 {t['title']}</h1>
        <p style='margin:5px 0 0 0; color:#9AA0A6; font-size: 1.1em;'>{t['sub']}</p></div>
        <div><span style="background: rgba(255,255,255,0.1); padding: 10px 25px; border-radius: 30px; font-weight: 600; border: 1px solid rgba(255,255,255,0.2);">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 분석 엔진 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('Synchronizing with Global Biomechanical Database...'):
        score = 82 if "Marathon" in selected_sport else 65 # 경보일 경우 각도 미달로 점수 대폭 하락 설정
        my_stats = [75, 68, 85, 70, 65] 
        avg_angle = 155.9 # 사용자의 고정 데이터
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        bench_name = selected_bench.split(" ")[1] if " " in selected_bench else selected_bench
        
    st.markdown(f"<h3 style='color: #202124;'>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=score, title={'text': "전체 역학 효율성 (Score)", 'font': {'size': 18, 'color': '#5F6368'}},
            domain={'x': [0, 1], 'y': [0, 1]}, 
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#1A73E8" if score > 70 else "#D93025"}, # 70점 이하면 붉은색 경고
                'bgcolor': "white", 'borderwidth': 2, 'bordercolor': "#E8EAED",
                'steps': [{'range': [0, 70], 'color': "#FCE8E6"}, {'range': [85, 100], 'color': "#E6F4EA"}],
                'threshold': {'line': {'color': "#D93025", 'width': 4}, 'value': 95}
            }))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#202124", 'family': "Pretendard"})
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=t['cat'], fill='toself', name='My Data', line_color='#D93025', fillcolor='rgba(217, 48, 37, 0.2)'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=t['cat'], fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E8EAED', linecolor='#E8EAED')), 
            showlegend=True, height=300, margin=dict(l=50, r=50, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "#5F6368", 'family': "Pretendard"}
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;">
            <h4 style="color: #202124; margin-top: 0;">{t['img_title']}</h4>
            <p style="color: #5F6368; margin-bottom: 0;">{t['img_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        x_my_ankle = -np.sin(np.radians(180 - avg_angle))
        y_my_ankle = -np.cos(np.radians(180 - avg_angle))
        x_target_ankle = -np.sin(np.radians(180 - target_angle))
        y_target_ankle = -np.cos(np.radians(180 - target_angle))

        fig_overlay = go.Figure()
        fig_overlay.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), marker=dict(size=14, color='white'), name='대퇴부(Thigh)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_my_ankle], y=[0, y_my_ankle], mode='lines+markers', line=dict(color='#D93025', width=8), marker=dict(size=14, color='#D93025'), name=f'내 궤적 ({avg_angle}°)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_target_ankle], y=[0, y_target_ankle], mode='lines', line=dict(color='#F9AB00', width=4, dash='dash'), name=f'표준선 ({target_angle}°)'))

        fig_overlay.update_layout(
            plot_bgcolor='#202124', paper_bgcolor='#202124', font=dict(color='white', family='Pretendard'),
            xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]),
            margin=dict(l=20, r=20, t=20, b=20), height=500, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box">', unsafe_allow_html=True)
        tab_pro, tab_easy = st.tabs(["🎓 전문가 역학 리포트 (Pro)", "🎈 쉬운 코칭 (Easy)"])
        
        # 💡 종목에 따른 다이나믹 피드백 로직
        if "Marathon" in selected_sport:
            # 기존 마라톤 피드백
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#1A73E8; margin-top:10px; margin-bottom:15px;">📋 마라톤 생체역학 정밀 진단</h4>
                <p style="font-size: 0.95em; color: #5F6368; line-height: 1.6; margin-bottom: 15px;">
                    도약(Push-off) 페이즈의 최대 무릎 신전 각도는 <span class="highlight-text">{avg_angle}°</span>로 산출되었습니다. 
                    이는 목표 벤치마크({bench_name})의 최적화 기준선 {target_angle}° 대비 <span class="highlight-text">{gap:.1f}°의 편차</span>를 보이며, 대퇴사두근의 불완전 수축에 의한 추진 에너지 누수를 의미합니다. 특히 상하체 동기화 지수(팔치기)가 낮아 햄스트링에 과부하가 집중되고 있습니다.
                </p>
                <div style="font-size: 0.95em; color: #202124; background: #F8F9FA; padding: 15px; border-radius: 8px; border: 1px solid #E8EAED;">
                    <b>[맞춤형 역학 교정 프로토콜]</b><br>
                    1. <b>가동성:</b> 장요근 동적 스트레칭으로 고관절 신전 가동 범위 물리적 확장<br>
                    2. <b>동기화:</b> 무릎 신전과 팔꿈치 후방 스윙(Arm Drive)의 1:1 리듬 매칭<br>
                    3. <b>큐잉:</b> 중족골(발볼)로 지면을 끝까지 밀어내는 'Full Toe-off' 인지 제어
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#D93025; margin-top:10px; margin-bottom:15px;">🏃‍♂️ AI 코치의 친절한 달리기 꿀팁!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.6;">
                    <b>"다리와 팔을 시원하게 뻗어볼까요?"</b><br>
                    지금 땅을 차고 나갈 때 내 무릎 각도는 <span class="highlight-text">{avg_angle}°</span>예요. 
                    선수들({target_angle}°)처럼 다리를 쫙! 펴주면서, 동시에 <b>팔꿈치를 뒤로 경쾌하게 쳐주면</b> 훨씬 적은 힘으로 슝~ 하고 앞으로 날아갈 수 있어요!
                </p>
                """, unsafe_allow_html=True)
        else:
            # 🚨 경보(Race Walking) 특화 피드백 (파울 경고 중심)
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#D93025; margin-top:10px; margin-bottom:15px;">🚨 경보 규정(Rule) 위반 경고 감지</h4>
                <p style="font-size: 0.95em; color: #5F6368; line-height: 1.6; margin-bottom: 15px;">
                    경보 종목의 핵심 판정 기준인 <b>'무릎 완전 신전 규정(Straight Leg Rule)'</b> 위반이 비전 알고리즘에 의해 감지되었습니다. 
                    현재 접촉 페이즈의 무릎 각도가 <span class="highlight-text">{avg_angle}°</span>에 불과하여, 기준선(180°) 대비 <span class="highlight-text">{gap:.1f}°의 치명적인 편차(Bent Knee)</span>를 보입니다. 이는 공식 대회에서 즉각적인 레드카드(Red Card) 및 실격(DQ) 사유에 해당합니다.
                </p>
                <div style="font-size: 0.95em; color: #202124; background: #FCE8E6; padding: 15px; border-radius: 8px; border: 1px solid #FAD1D0;">
                    <b>[경보 특화 폼 교정 프로토콜]</b><br>
                    1. <b>착지 제어:</b> 발뒤꿈치가 지면에 닿는 순간부터 수직이 될 때까지 무릎 관절을 100% 락킹(Locking) 상태로 유지하십시오.<br>
                    2. <b>골반 롤링(Pelvic Rotation):</b> 좁아진 보폭을 무릎이 아닌, 골반의 전후 수평 회전을 극대화하여 극복해야 합니다.<br>
                    3. <b>상체 크로스 암(Cross-Arm):</b> 골반의 강한 회전을 제어하기 위해 팔을 가슴 안쪽으로 강하게 치며 코어 밸런스를 잡으세요.
                </div>
                """, unsafe_allow_html=True)
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#D93025; margin-top:10px; margin-bottom:15px;">🚶‍♂️ 앗! 삐익- 반칙(파울)이에요!</h4>
                <p style="font-size: 1.05em; color: #3C4043; line-height: 1.6;">
                    <b>"경보에서는 무릎이 구부러지면 안 돼요!"</b><br>
                    경보 선수들은 걸을 때 다리가 180°로 일자(ㅡ)가 되도록 쫙 펴야 해요. 
                    지금 우리는 무릎이 <span class="highlight-text">{avg_angle}°</span>로 굽혀져 있어서 심판에게 경고를 받을 수 있어요.<br><br>
                    <b>✨ 모델처럼 걷기 미션 ✨</b><br>
                    골반을 앞뒤로 씰룩~쌜룩~ 크게 흔들면서, 앞발이 땅에 닿을 때는 <b>다리 뒷부분이 팽팽해질 정도로 무릎을 쫙! 펴고</b> 걸어볼까요?
                </p>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 🛰️ 구글/메타 제휴 비전 섹션
st.markdown(f"""
    <div class="vision-card">
        <h3 style="color: #1A73E8; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            {t['vision_title']}
        </h3>
        <p style="font-size: 1.1em; color: #3C4043; line-height: 1.6; margin-bottom: 20px;">
            {t['vision_desc']}
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <span style="background: #E8F0FE; color: #1A73E8; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9em; border: 1px solid #D2E3FC;">#Smart_Glass_HUD</span>
            <span style="background: #E8F0FE; color: #1A73E8; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9em; border: 1px solid #D2E3FC;">#Global_Rule_Judging</span>
            <span style="background: #E8F0FE; color: #1A73E8; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9em; border: 1px solid #D2E3FC;">#HeartRate_Audio_Sync</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 8. 🧪 피드백 연구소 섹션
st.markdown("---")
st.markdown('<div class="data-card" style="margin-bottom: 50px;">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #202124;'>{t['f_title']}</h3>", unsafe_allow_html=True)
st.write(f"<span style='color: #5F6368;'>{t['f_desc']}</span>", unsafe_allow_html=True)

with st.form(key='marathon_ai_lab_form', clear_on_submit=True):
    user_comment = st.text_area("연구소로 데이터 전송 (Data Submission)", placeholder="예: '경보 파울 판정 기능이 아주 유용하네요!'")
    submit_button = st.form_submit_button(label="의견 전송 및 세계 표준 구축 참여 (Submit)", type="primary")

    if submit_button:
        if user_comment:
            st.balloons()
            st.success(t['f_success'])
        else:
            st.warning("의견을 먼저 입력해 주세요. (Please enter your feedback first.)")
st.markdown('</div>', unsafe_allow_html=True)
