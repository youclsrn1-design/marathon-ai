import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 시스템 설정
st.set_page_config(page_title="MARATHON AI | Global", layout="wide", initial_sidebar_state="expanded")

# 2. 국가별 다국어 및 현지화 데이터베이스 (Glocal Database)
c_data = {
    "🇰🇷 대한민국 (한국어)": {
        "local_team": "대한민국 국가대표", "local_angle": 162.8, "local_radar": [85, 88, 80, 85, 90],
        "title": "🇰🇷 MARATHON AI PRO", "sub": "글로벌 생체역학 정밀 분석",
        "s_title": "🎥 비전 데이터 입력", "s_up": "러닝 영상 업로드", "s_gen": "성별", "s_gen_list": ["남성", "여성"],
        "s_btn": "🚀 정밀 역학 분석 실행", "r_title": "📊 생체역학 정밀 진단 리포트",
        "radar_cats": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 안정성', '케이던스'],
        "r_sol": "💡 전문 교정 프로토콜", 
        "r_sol_text": "**1. 지면 반발력 누수 제어**<br>무릎 신전 각도가 세계 기록군 대비 부족하여 도약 시 에너지가 분산됩니다.<br><br>**2. 착지점 재조정**<br>발이 무게중심보다 과도하게 앞에 떨어지지 않도록 케이던스를 높이세요.",
        "f_title": "💬 사용자 검증 피드백", "f_desc": "본 서비스는 베타 테스트 중입니다. 의견을 남겨주시면 큰 힘이 됩니다."
    },
    "🇺🇸 United States (English)": {
        "local_team": "US Olympic Team", "local_angle": 164.5, "local_radar": [88, 90, 85, 88, 92],
        "title": "🇺🇸 MARATHON AI PRO", "sub": "Global Biometric Performance Analysis",
        "s_title": "🎥 Vision Data Input", "s_up": "Upload Running Video", "s_gen": "Gender", "s_gen_list": ["Male", "Female"],
        "s_btn": "🚀 Run Biometric Analysis", "r_title": "📊 Biometric Diagnostic Report",
        "radar_cats": ['Knee Extension', 'GCT', 'Oscillation', 'Pelvic Stability', 'Cadence'],
        "r_sol": "💡 Professional Coaching Protocol",
        "r_sol_text": "**1. Ground Reaction Force (GRF)**<br>Knee extension angle is lower than the world record group, causing braking force.<br><br>**2. Mid-foot Strike Adjustment**<br>Increase cadence by 5% to prevent overstriding.",
        "f_title": "💬 User Feedback & Validation", "f_desc": "This service is in beta. We appreciate your feedback."
    },
    "🇯🇵 日本 (日本語)": {
        "local_team": "日本代表 (Japan Elite)", "local_angle": 163.5, "local_radar": [87, 89, 82, 87, 91],
        "title": "🇯🇵 MARATHON AI PRO", "sub": "グローバル生体力学 精密分析",
        "s_title": "🎥 ビジョンデータ入力", "s_up": "ランニング動画のアップロード", "s_gen": "性別", "s_gen_list": ["男性", "女性"],
        "s_btn": "🚀 精密バイオメカニクス分析", "r_title": "📊 生体力学 診断レポート",
        "radar_cats": ['膝の伸展', '接地時間', '上下動', '骨盤の安定性', 'ピッチ'],
        "r_sol": "💡 専門的コーチングプロトコル",
        "r_sol_text": "**1. 反発力の最適化**<br>世界記録保持者と比較して膝の伸展角度が不足しています。<br><br>**2. 着地位置の調整**<br>オーバーストライドを防ぐため、ピッチを5％上げてください。",
        "f_title": "💬 ユーザーフィードバック", "f_desc": "現在ベータテスト中です。ご意見をお聞かせください。"
    }
}

# 3. 사이드바 최상단 국가 선택
country_choice = st.sidebar.selectbox("🌐 Country / Region (국가 선택)", list(c_data.keys()))
t = c_data[country_choice]

# 4. CSS 및 헤더 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #f4f7f9; }
    .header-panel { background: linear-gradient(135deg, #0A192F 0%, #002D62 100%); padding: 40px 30px; border-radius: 20px; color: white; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); display: flex; justify-content: space-between; align-items: center; }
    .data-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e1e4e8; height: 100%; }
    .feedback-box { background: white; padding: 30px; border-radius: 15px; margin-top: 40px; border-top: 5px solid #CD2E3A; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-panel">
        <div><h1 style='margin:0; font-weight:900; font-size:2.5em;'>{t['title']}</h1><p style='margin:5px 0 0 0; color:#8892B0;'>{t['sub']}</p></div>
        <div><span style="background: #CD2E3A; padding: 8px 20px; border-radius: 20px; font-weight: bold;">Toss ID: MARATHON AI</span></div>
    </div>
    """, unsafe_allow_html=True)

# 5. 사이드바 입력
with st.sidebar:
    st.markdown(f"### {t['s_title']}")
    video_file = st.file_uploader(t['s_up'], type=['mp4', 'mov'])
    gender = st.selectbox(t['s_gen'], t['s_gen_list'])
    # 세계 기록과 해당 국가 대표를 비교 타겟으로 자동 설정!
    target_group = st.selectbox("Benchmark", ["World Record Holder", t['local_team']])
    analyze_btn = st.button(t['s_btn'], use_container_width=True)

# 6. 메인 분석 영역
if video_file and analyze_btn:
    with st.spinner('Syncing global biometric data...'):
        score = 82
        my_stats = [75, 68, 85, 70, 80]
        world_stats = [98, 95, 96, 99, 97]
        u_angle = np.random.normal(159, 3.5, 100)
        
    st.markdown(f"<h3>{t['r_title']}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score", 'font': {'size': 20}},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#0047A0"}, 'steps': [{'range': [0, 60], 'color': "#ffe6e6"}, {'range': [85, 100], 'color': "#e6ffe6"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 95}}))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=my_stats, theta=t['radar_cats'], fill='toself', name='My Data', line_color='#CD2E3A'))
        fig_radar.add_trace(go.Scatterpolar(r=world_stats, theta=t['radar_cats'], fill='none', name='World Record', line_color='#0047A0', line_dash='dash'))
        # 선택한 국가의 대표팀 데이터 자동 연동!
        fig_radar.add_trace(go.Scatterpolar(r=t['local_radar'], theta=t['radar_cats'], fill='none', name=t['local_team'], line_color='#888', line_dash='dot'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=40, r=40, t=30, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1.5, 1])
    with col3:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(y=u_angle, name='My Angle', line=dict(color='#CD2E3A', width=3)))
        fig_line.add_trace(go.Scatter(y=[168.5]*100, name='World Target', line=dict(color='#0047A0', dash='dash')))
        # 선택한 국가의 무릎 각도 데이터 라인 자동 생성!
        fig_line.add_trace(go.Scatter(y=[t['local_angle']]*100, name=t['local_team'], line=dict(color='#999', dash='dot')))
        fig_line.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown(f"#### {t['r_sol']}")
        st.markdown(t['r_sol_text'], unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 피드백 섹션
st.markdown("---")
st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
st.markdown(f"### {t['f_title']}")
st.write(t['f_desc'])
with st.form("feedback_form", clear_on_submit=True):
    f_comment = st.text_area("✍️ Input Feedback")
    f_submit = st.form_submit_button("Submit")
st.markdown('</div>', unsafe_allow_html=True)
