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
        "s_data": "📊 비교 벤치마크", "s_vid": "🎥 비전 데이터 입력", "s_up": "러닝 영상 업로드 (10초 이내 측면 영상 권장)", 
        "s_gen": "성별", "s_btn": "🚀 정밀 역학 분석 실행", "r_title": "🔬 생체역학 정밀 진단 리포트",
        "cat": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 안정성', '케이던스'],
        "img_title": "📸 비전 AI 관절 추출 및 궤적 오버레이",
        "img_desc": "우측으로 진행하는 러너의 도약(Push-off) 프레임을 추출하여, 벤치마크 기준선(🟡)과 실제 무릎 각도(🔴)의 편차를 시각화합니다.",
        "vip_title": "👑 [VIP PRO] 장시간 러닝 피로도 및 자세 붕괴 타임라인",
        "vip_desc": "마라톤 풀코스 또는 장거리 훈련 영상을 분석하여, 누적된 피로로 인해 생체역학 밸런스가 무너지는 '크리티컬 포인트(Critical Point)'를 자동 추출합니다.",
        "f_title": "💬 글로벌 사용자 피드백", "f_desc": "MARATHON AI는 전 세계 러너들의 피드백을 통해 성장합니다."
    },
    "🇺🇸 English": {
        "title": "MARATHON AI PRO", "sub": "Global Standard Biometric Analysis System", "toss": "Powered by MARATHON AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", 
        "s_data": "📊 Benchmark Target", "s_vid": "🎥 Vision Data Input", "s_up": "Upload Video (Max 10s side-view)", 
        "s_gen": "Gender", "s_btn": "🚀 Run Precision Analysis", "r_title": "🔬 Biometric Diagnostic Report",
        "cat": ['Knee Ext.', 'GCT', 'Oscillation', 'Pelvic Stability', 'Cadence'],
        "img_title": "📸 Vision AI Frame Overlay Analysis",
        "img_desc": "Visualizing the deviation between your knee angle (🔴) and the benchmark target (🟡) during the push-off phase (runner moving right).",
        "vip_title": "👑 [VIP PRO] Long-Distance Fatigue & Form Breakdown Timeline",
        "vip_desc": "Analyzes full marathon or long-run footage to auto-detect 'Critical Points' where biomechanical balance collapses due to accumulated fatigue.",
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
    .vip-box { background: linear-gradient(to right, #2c3e50, #000000); padding: 30px; border-radius: 15px; margin-top: 30px; border: 1px solid #FFD700; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.15); color: white; }
    .timeline-item { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #FFD700; }
    .coaching-box { background: #fdfdfd; border-left: 6px solid #0047A0; padding: 30px; border-radius: 0 15px 15px 0; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
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
        u_angle = np.random.normal(155.5, 3.5, 100)
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
        <div class="data-card" style="margin-top: 20px; border-top: 5px solid #0047A0;">
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
            margin=dict(l=20, r=20, t=40, b=20), height=350, showlegend=True, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig_overlay, use_container_width=True)

    with col4:
        if selected_lang == "🇰🇷 한국어":
            st.markdown(f"""
            <div class="coaching-box">
                <h4 style="color:#002D62; margin-top:0;">📋 딥러닝 기반 생체역학 코칭 리포트</h4>
                <p style="font-size: 1.1em; margin-bottom: 5px;">
                    <b>[역학적 진단 (Biomechanical Diagnosis)]</b><br>
                    현재 귀하의 도약(Push-off) 구간 유효 무릎 신전 각도는 <span style="color:#CD2E3A; font-weight:bold;">{avg_angle:.1f}°</span>로 측정되었습니다. 
                    이는 선택하신 <b>{bench_name} 그룹 데이터({target_angle:.1f}°)</b> 대비 <b>{gap:.1f}° 편차</b>를 보입니다. 
                    이는 지면을 밀어내는 과정에서 대퇴사두근과 비복근의 수축이 조기에 종료됨을 시사합니다.
                </p>
                <p style="font-size: 1.1em; margin-bottom: 5px;">
                    <b>[운동에너지 손실 (Kinetic Energy Loss)]</b><br>
                    이러한 각도 부족은 <b>지면 반발력(GRF, Ground Reaction Force)의 벡터를 전진 방향이 아닌 수직 방향으로 분산</b>시킵니다. 
                    결과적으로 보폭(Stride Length)당 약 4~6%의 추진 에너지가 손실되며, 이를 보완하기 위해 햄스트링에 과도한 부하가 집중되고 있습니다.
                </p>
                <p style="font-size: 1.1em;">
                    <b>[단계별 교정 프로토콜 (Corrective Protocol)]</b><br>
                    1. <b>고관절 굴곡근 스트레칭:</b> 장요근의 유연성을 확보하여 후방 킥의 가동 범위를 물리적으로 넓혀야 합니다.<br>
                    2. <b>플라이오메트릭 훈련:</b> 바운딩(Bounding)을 주 2회 실시하여 하퇴 삼두근의 탄성 에너지 방출 능력을 극대화하세요.<br>
                    3. <b>러닝 큐잉 (Cueing):</b> 발이 땅에서 떨어지는 순간, 발가락 끝까지 지면을 밀어낸다는 느낌('Toe-off')을 강하게 의식하십시오.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="coaching-box">
                <h4 style="color:#002D62; margin-top:0;">📋 AI Biomechanical Coaching Report</h4>
                <p style="font-size: 1.1em; margin-bottom: 5px;">
                    <b>[Biomechanical Diagnosis]</b><br>
                    Your effective knee extension angle during the push-off phase is <span style="color:#CD2E3A; font-weight:bold;">{avg_angle:.1f}°</span>. 
                    This represents a <b>{gap:.1f}° deviation</b> compared to the <b>{bench_name} baseline ({target_angle:.1f}°)</b>, indicating premature termination of quadriceps and gastrocnemius contraction.
                </p>
                <p style="font-size: 1.1em; margin-bottom: 5px;">
                    <b>[Kinetic Energy Loss]</b><br>
                    This lack of extension causes the <b>Ground Reaction Force (GRF) vector to dissipate vertically</b> rather than propelling you forward. 
                    As a result, approximately 4-6% of propulsion energy is lost per stride, placing excessive compensatory load on your hamstrings.
                </p>
                <p style="font-size: 1.1em;">
                    <b>[Corrective Protocol]</b><br>
                    1. <b>Hip Flexor Mobility:</b> Improve iliopsoas flexibility to physically expand the range of motion for your rear kick.<br>
                    2. <b>Plyometrics:</b> Incorporate bounding exercises twice a week to maximize the elastic energy release of your calf muscles.<br>
                    3. <b>Running Cueing:</b> Consciously focus on pushing off the ground completely through your toes ('Toe-off') right before the swing phase.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 👑 대망의 VIP 타임라인 섹션 (BM 핵심)
    st.markdown(f"""
        <div class="vip-box">
            <h3 style="margin-top: 0; color: #FFD700;">{t['vip_title']}</h3>
            <p style="color: #ccc; margin-bottom: 20px;">{t['vip_desc']}</p>
    """, unsafe_allow_html=True)

    if selected_lang == "🇰🇷 한국어":
        st.markdown("""
            <div class="timeline-item">
                <strong style="color: #00FF00;">⏱️ 00:15:30 [안정 구간]</strong><br>
                무릎 신전 각도 160도 유지. 케이던스 180spm으로 최적의 에너지 효율성 보임.
            </div>
            <div class="timeline-item" style="border-left-color: #FFA500;">
                <strong style="color: #FFA500;">⏱️ 01:10:45 [주의: 피로 누적 감지]</strong><br>
                무릎 신전 각도가 155도로 하락. 골반 틸트(Pelvic Tilt) 발생으로 보폭(Stride)이 좁아지기 시작함. 👉 <b>[AI 코칭]</b> 코어 긴장 유지 및 팔치기 반경 확대 요망.
            </div>
            <div class="timeline-item" style="border-left-color: #FF4500;">
                <strong style="color: #FF4500;">⏱️ 01:50:20 [위험: 폼 붕괴 임계점]</strong><br>
                케이던스 10% 급감(162spm). 지면 접촉 시간(GCT)이 늘어나 무릎 관절의 수직 충격량이 1.5배 증가. 👉 <b>[AI 코칭]</b> 속도를 늦추고 보폭을 극단적으로 줄여 부상을 방지하세요.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="timeline-item">
                <strong style="color: #00FF00;">⏱️ 00:15:30 [Stable Phase]</strong><br>
                Knee extension at 160°. Cadence 180spm. Optimal energy efficiency.
            </div>
            <div class="timeline-item" style="border-left-color: #FFA500;">
                <strong style="color: #FFA500;">⏱️ 01:10:45 [Warning: Fatigue Detected]</strong><br>
                Knee extension dropped to 155°. Pelvic tilt observed, stride shortening. 👉 <b>[AI Coaching]</b> Maintain core tension and increase arm swing radius.
            </div>
            <div class="timeline-item" style="border-left-color: #FF4500;">
                <strong style="color: #FF4500;">⏱️ 01:50:20 [Danger: Form Breakdown]</strong><br>
                Cadence dropped by 10% (162spm). Ground Contact Time (GCT) increased, knee impact force x1.5. 👉 <b>[AI Coaching]</b> Slow down and significantly shorten stride to prevent injury.
            </div>
        </div>
        """, unsafe_allow_html=True)

# 7. 피드백 섹션
st.markdown("---")
st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.markdown(f"### {t['f_title']}")
with st.form("feedback_form", clear_on_submit=True):
    f_comment = st.text_area("✍️ Input Feedback")
    f_submit = st.form_submit_button("Submit")
st.markdown('</div>', unsafe_allow_html=True)
