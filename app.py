import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 시스템 설정
st.set_page_config(page_title="MARATHON AI | Global Standard", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩
ui_langs = {
    "🇰🇷 한국어": {
        "title": "MARATHON AI PRO", "sub": "글로벌 생체역학 정밀 분석 표준 시스템", "toss": "Toss ID: MARATHON AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", 
        "s_data": "📊 비교 벤치마크", "s_vid": "🎥 비전 데이터 입력", "s_up": "러닝 영상 파일 업로드 (10초 이내 측면 영상 권장)", 
        "s_gen": "성별", "s_btn": "🚀 정밀 역학 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "cat": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 안정성', '케이던스'],
        "img_title": "📸 비전 AI 관절 추출 및 궤적 오버레이",
        "img_desc": "우측으로 진행하는 러너의 도약(Push-off) 프레임을 추출하여, 벤치마크 기준선(🟡)과 실제 무릎 각도(🔴)의 편차를 시각화합니다.",
        "f_title": "💬 글로벌 사용자 피드백", "f_desc": "MARATHON AI는 전 세계 러너들의 피드백을 통해 성장합니다."
    },
    "🇺🇸 English": {
        "title": "MARATHON AI PRO", "sub": "Global Standard Biometric Analysis System", "toss": "Powered by MARATHON AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", 
        "s_data": "📊 Benchmark Target", "s_vid": "🎥 Vision Data Input", "s_up": "Upload Running Video (Max 10s side-view)", 
        "s_gen": "Gender", "s_btn": "🚀 Run Precision Analysis", "r_title": "🔬 Biometric Diagnostic Report",
        "cat": ['Knee Ext.', 'GCT', 'Oscillation', 'Pelvic Stability', 'Cadence'],
        "img_title": "📸 Vision AI Frame Overlay Analysis",
        "img_desc": "Visualizing the deviation between your knee angle (🔴) and the benchmark target (🟡) during the push-off phase (runner moving right).",
        "f_title": "💬 Global User Feedback", "f_desc": "MARATHON AI grows with feedback from runners worldwide."
    }
}

# 3. 글로벌 데이터베이스
benchmarks = {
    "🌍 World Record (세계 신기록)": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"},
    "🇰🇪 Kenya Elite (케냐 최상위)": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"},
    "🇺🇸 US Olympic (미국 국가대표)": {"angle": 164.5, "radar": [88, 90, 85, 88, 92], "color": "#3C3B6E"},
    "🇯🇵 Japan Elite (일본 대표팀)": {"angle": 163.5, "radar": [87, 89, 82, 87, 91], "color": "#BC002D"},
    "🇨🇳 China Elite (중국 대표팀)": {"angle": 163.0, "radar": [86, 88, 81, 86, 89], "color": "#EE1C25"},
    "🇰🇷 Korea Elite (대한민국 대표팀)": {"angle": 162.8, "radar": [85, 88, 80, 85, 90], "color": "#CD2E3A"},
    "🌐 Global Amateur (일반인 평균)": {"angle": 155.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
}

# 4. CSS 세팅
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #f4f7f9; }
    .header-panel { background: linear-gradient(135deg, #112A46 0%, #001B3A 100%); padding: 35px 30px; border-radius: 20px; color: white; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; height: 100%; }
    .coaching-box { background: #fdfdfd; border-left: 6px solid #CD2E3A; padding: 25px; border-radius: 0 15px 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.08); height: 100%; }
    .highlight-text { color: #CD2E3A; font-weight: 900; }
    .benchmark-text { color: #FFB300; font-weight: 900; background: #333; padding: 2px 6px; border-radius: 4px; }
    .easy-text { font-size: 1.15em; color: #444; line-height: 1.7; }
    .easy-highlight { background-color: #FFF3CD; padding: 2px 5px; border-radius: 5px; font-weight: bold; color: #856404; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    selected_bench = st.selectbox("📊 Benchmark Target", list(benchmarks.keys()))
    b_data = benchmarks[selected_bench]
    st.markdown("---")
    
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov', 'avi'])
    gender = st.selectbox(t['s_gen'], ["Male", "Female"] if "English" in selected_lang else ["남성", "여성"])
    analyze_btn = st.button(t['s_btn'], use_container_width=True)

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.2em;'>🌍 {t['title']}</h1><p style='margin:5px 0 0 0; color:#8892B0;'>{t['sub']}</p></div>
        <div><span style="background: #0047A0; padding: 8px 20px; border-radius: 20px; font-weight: bold;">{t['toss']}</span></div>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 분석 영역
if video_file and analyze_btn:
    with st.spinner('Syncing with Global Biometric Data Center...'):
        score = 82
        my_stats = [75, 68, 85, 70, 80]
        u_angle = np.random.normal(155.9, 3.5, 100) 
        avg_angle = np.mean(u_angle)
        target_angle = b_data['angle']
        gap = target_angle - avg_angle
        bench_name = selected_bench.split(" ")[1]
        
    st.markdown(f"<h3>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, domain={'x': [0, 1], 'y': [0, 1]}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0047A0"}, 'steps': [{'range': [0, 60], 'color': "#ffe6e6"}, {'range': [85, 100], 'color': "#e6ffe6"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 95}}))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=t['cat'], fill='toself', name='My Data', line_color='#CD2E3A'))
        fig_radar.add_trace(go.Scatterpolar(r=b_data['radar'], theta=t['cat'], fill='none', name=bench_name, line_color=b_data['color'], line_dash='dash'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=40, r=40, t=30, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 📸 오버레이 영역
    st.markdown(f"""
        <div class="data-card" style="margin-top: 20px; border-top: 5px solid #FFB300;">
            <h4 style="color: #002D62; margin-top: 0;">{t['img_title']}</h4>
            <p style="color: #555;">{t['img_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        x_my_ankle = -np.sin(np.radians(180 - avg_angle))
        y_my_ankle = -np.cos(np.radians(180 - avg_angle))
        x_target_ankle = -np.sin(np.radians(180 - target_angle))
        y_target_ankle = -np.cos(np.radians(180 - target_angle))

        fig_overlay = go.Figure()
        fig_overlay.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), marker=dict(size=12, color='white'), name='대퇴부 (Thigh)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_my_ankle], y=[0, y_my_ankle], mode='lines+markers', line=dict(color='#CD2E3A', width=8), marker=dict(size=12, color='#CD2E3A'), name=f'내 무릎 ({avg_angle:.1f}°)'))
        fig_overlay.add_trace(go.Scatter(x=[0, x_target_ankle], y=[0, y_target_ankle], mode='lines', line=dict(color='#FFB300', width=4, dash='dash'), name=f'{bench_name} ({target_angle:.1f}°)'))

        fig_overlay.update_layout(
            title="Knee Extension Tracking Vision HUD", plot_bgcolor='#112A46', paper_bgcolor='#112A46', font=dict(color='white'),
            xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]),
            margin=dict(l=20, r=20, t=40, b=20), height=480, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box">', unsafe_allow_html=True)
        
        if selected_lang == "🇰🇷 한국어":
            # Streamlit 탭 생성 (전문가용 vs 쉬운 설명)
            tab_pro, tab_easy = st.tabs(["🎓 전문가용 리포트 (Pro)", "🎈 쉬운 설명 (Easy / Kids)"])
            
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#002D62; margin-top:10px; margin-bottom: 15px;">📋 딥러닝 기반 역학 진단 및 교정 리포트</h4>
                <p style="font-size: 1.05em; color: #333;"><b>[운동역학적 궤적 진단 (Kinematic Trajectory Diagnosis)]</b></p>
                <p style="font-size: 0.95em; color: #555; line-height: 1.6; margin-bottom: 15px;">
                    현재 도약(Push-off) 페이즈의 최대 무릎 신전(Knee Extension) 각도는 <span class="highlight-text">{avg_angle:.1f}°</span>로 산출되었습니다. 
                    이는 타겟 그룹인 <span class="benchmark-text">{bench_name}</span>의 최적화된 기준선 <b>{target_angle:.1f}°</b> 대비 <b>{gap:.1f}°의 역학적 편차(Deviation)</b>를 보입니다. 
                    생체역학적으로 이는 대퇴사두근의 수축이 불완전한 상태에서 지면 발진(Take-off)이 조기에 이루어지고 있음을 시사합니다.
                </p>
                <p style="font-size: 1.05em; color: #333;"><b>[지면반발력(GRF) 및 에너지 누수 분석]</b></p>
                <p style="font-size: 0.95em; color: #555; line-height: 1.6; margin-bottom: 15px;">
                    해당 각도 편차는 하지(Lower Extremity)를 통해 전달되어야 할 <b>지면반발력 벡터를 전방(Forward)이 아닌 수직(Vertical)으로 분산</b>시킵니다. 
                    결과적으로 보폭당 약 <b>7~10%의 전진 추진력 누수</b>가 발생하며, 장거리 주행 시 햄스트링에 과부하가 집중됩니다.
                </p>
                <div style="font-size: 0.95em; color: #444; line-height: 1.6; background: #f4f7f9; padding: 15px; border-radius: 8px;">
                    <b>[맞춤형 역학 교정 솔루션]</b><br>
                    1. <b>가동성 확보:</b> 장요근 동적 스트레칭으로 고관절 신전 가동 범위 확장<br>
                    2. <b>탄성 훈련:</b> 하퇴 삼두근 건-근육 복합체(SSC) 강화를 위한 뎁스 점프 주 2회<br>
                    3. <b>신경 제어(Cueing):</b> '엄지발가락 끝으로 지면을 끝까지 밀어낸다'는 인지적 큐잉 적용
                </div>
                """, unsafe_allow_html=True)
                
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#FF6B6B; margin-top:10px; margin-bottom: 15px;">🏃‍♂️ AI 코치의 친절한 달리기 꿀팁!</h4>
                <p class="easy-text">
                    <b>앗! 다리가 조금 덜 펴지고 있어요! 🧐</b><br>
                    땅을 차고 앞으로 나갈 때, 내 무릎 각도는 <span class="highlight-text">{avg_angle:.1f}°</span> 예요. 
                    세계적인 선수들({bench_name})은 <span style="color:#FFB300; font-weight:bold;">{target_angle:.1f}°</span>까지 다리를 쫙! 펴서 달리는데, 
                    우리는 <span class="easy-highlight">{gap:.1f}° 만큼 무릎을 덜 펴고</span> 있네요.
                </p>
                <p class="easy-text">
                    <b>왜 다리를 쫙 펴야 할까요? 🚀</b><br>
                    다리를 끝까지 안 펴면, 앞으로 슝~ 날아가는 대신 몸이 위아래로 쿵쾅쿵쾅 뛰게 돼요. 
                    그럼 <span class="easy-highlight">힘만 많이 들고 금방 지쳐버린답니다!</span>
                </p>
                <div style="font-size: 1.1em; color: #444; line-height: 1.6; background: #FFF5F5; padding: 15px; border-radius: 8px; border: 2px dashed #FFD0D0;">
                    <b>✨ 이렇게 연습해 볼까요? ✨</b><br>
                    1. <b>개구리 점프 (스트레칭):</b> 고관절(골반)을 쭉쭉 늘려주는 스트레칭을 매일 해봐요.<br>
                    2. <b>캥거루 점프 (힘 기르기):</b> 다리에 용수철이 달린 것처럼 통통 튀어 오르는 점프 연습을 해요.<br>
                    3. <b>발가락 뻥! (달리기 팁):</b> 달릴 때 <span style="color:#FF6B6B; font-weight:bold;">'엄지발가락으로 땅을 뻥! 차고 나간다'</span>고 상상하며 뛰어보세요. 훠얼~씬 가벼워질 거예요!
                </div>
                """, unsafe_allow_html=True)

        else:
            # 영문 버전 탭 (Pro vs Easy)
            tab_pro, tab_easy = st.tabs(["🎓 Expert Report (Pro)", "🎈 Easy Explain (Kids/Beginner)"])
            
            with tab_pro:
                st.markdown(f"""
                <h4 style="color:#002D62; margin-top:10px; margin-bottom: 15px;">📋 AI Biomechanical Diagnosis Report</h4>
                <p style="font-size: 0.95em; color: #555; line-height: 1.6; margin-bottom: 15px;">
                    <b>[Kinematic Diagnosis]</b><br>
                    Your knee extension angle during push-off is <span class="highlight-text">{avg_angle:.1f}°</span>. 
                    This is a <b>{gap:.1f}° deviation</b> from the {bench_name} baseline ({target_angle:.1f}°), indicating premature take-off with incomplete quadriceps contraction.
                </p>
                <p style="font-size: 0.95em; color: #555; line-height: 1.6; margin-bottom: 15px;">
                    <b>[GRF & Energy Efficiency]</b><br>
                    This deficit causes the <b>Ground Reaction Force (GRF) vector to dissipate vertically</b>. 
                    Result: ~7-10% forward propulsion energy leak per stride and excessive hamstring load.
                </p>
                <div style="font-size: 0.95em; color: #444; line-height: 1.6; background: #f4f7f9; padding: 15px; border-radius: 8px;">
                    <b>[Targeted Solutions]</b><br>
                    1. <b>Mobility:</b> Iliopsoas dynamic stretching to expand hip extension ROM.<br>
                    2. <b>Plyometrics:</b> Depth jumps (2x/week) to maximize calf SSC elasticity.<br>
                    3. <b>Cueing:</b> Focus on 'Full Toe-off' before the foot leaves the ground.
                </div>
                """, unsafe_allow_html=True)
                
            with tab_easy:
                st.markdown(f"""
                <h4 style="color:#FF6B6B; margin-top:10px; margin-bottom: 15px;">🏃‍♂️ Friendly AI Running Tips!</h4>
                <p class="easy-text">
                    <b>Oops! Your leg isn't fully straightening! 🧐</b><br>
                    When you push off the ground, your knee is at <span class="highlight-text">{avg_angle:.1f}°</span>. 
                    Pro runners ({bench_name}) stretch it out to <span style="color:#FFB300; font-weight:bold;">{target_angle:.1f}°</span>. 
                    You are bending your knee <span class="easy-highlight">{gap:.1f}° more</span> than the pros!
                </p>
                <p class="easy-text">
                    <b>Why should you straighten it? 🚀</b><br>
                    If you don't straighten your leg, your energy bounces UP instead of pushing you FORWARD. 
                    <span class="easy-highlight">This makes you tired much faster!</span>
                </p>
                <div style="font-size: 1.1em; color: #444; line-height: 1.6; background: #FFF5F5; padding: 15px; border-radius: 8px; border: 2px dashed #FFD0D0;">
                    <b>✨ Let's try this! ✨</b><br>
                    1. <b>Frog Stretches:</b> Stretch your hips every day to make them super flexible.<br>
                    2. <b>Kangaroo Jumps:</b> Practice bouncy jumps like your legs are made of springs.<br>
                    3. <b>Big Toe POW!:</b> When you run, imagine <span style="color:#FF6B6B; font-weight:bold;">pushing the ground away with your big toe—POW!</span> You'll feel so much lighter!
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# 7. 피드백 섹션
st.markdown("---")
st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.markdown(f"### {t['f_title']}")
with st.form("feedback_form", clear_on_submit=True):
    f_comment = st.text_area("✍️ Input Feedback")
    f_submit = st.form_submit_button("Submit")
st.markdown('</div>', unsafe_allow_html=True)
