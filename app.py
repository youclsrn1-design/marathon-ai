import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 다국어 UI 및 코칭 언어팩 (올림픽 5대 언어)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "글로벌 육상 전 종목 생체역학 교육 시스템", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ 시스템 설정", "s_lang": "🌐 시스템 언어", "s_cat": "🏟️ 육상 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 비교 벤치마크", "s_up": "측면 영상 파일 선택 (10초 이내)", "s_btn": "🚀 AI 정밀 분석 및 지도법 생성", "r_title": "🔬 생체역학 진단 및 교육 리포트",
        "img_title": "📸 비전 AI 관절 추출 및 종목별 궤적 대조",
        "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 훈련 지도법",
        "c_sprint_pro": "<b>[단거리 역학]</b> 도약 시 무릎 신전이 {avg_angle}°에 그쳐 {gap:.1f}°의 조기 회수가 관찰됩니다. SSC(신장-단축 주기) 에너지가 누수 중입니다. <br><b>[훈련법]</b> 뎁스 점프를 통한 발목 반응성 극대화",
        "c_sprint_kids": "<b>[용암 밟기 놀이]</b> 무릎이 덜 펴졌어요! 바닥이 뜨거운 용암이라고 생각하고 앞꿈치로만 잽싸게 땅을 치고 지나가며 로켓처럼 튀어 나가세요!",
        "c_mara_pro": "<b>[마라톤 효율]</b> 무릎 완전 신전이 이루어지지 않아 {gap:.1f}° 편차 발생. GRF가 수직으로 분산됩니다.<br><b>[훈련법]</b> 장요근 동적 스트레칭 및 싱글 레그 데드리프트 수행",
        "c_mara_kids": "<b>[머리 위 물컵 지키기]</b> 쿵쾅거리면 물이 쏟아져요! 위아래로 흔들리지 말고 부드럽게 미끄러지듯 닌자처럼 사뿐사뿐 달려보세요.",
        "c_jump_pro": "<b>[도약 역학]</b> 마지막 걸음(Penultimate Step)에서 무게중심 하강비가 부족합니다.<br><b>[훈련법]</b> 힌지 제어를 통한 의도적 무게중심 하강 및 상향 스윙 매칭 훈련",
        "c_jump_kids": "<b>[마법의 징검다리]</b> 개구리처럼 뛰기 직전 무릎을 살짝 더 굽히고, 마지막 발이 닿는 순간 '쾅!' 밟으며 만세! 하고 솟아오르세요.",
        "c_throw_pro": "<b>[투척 역학]</b> 리드 레그의 블록킹 붕괴로 키네틱 체인이 단절되었습니다.<br><b>[훈련법]</b> 브레이싱 훈련 및 흉추 가동성 극대화를 통한 역학적 꼬임 확장",
        "c_throw_kids": "<b>[인간 투석기 놀이]</b> 얼음땡 던지기! 던지기 직전 앞발을 딛으며 '얼음!' 멈추고, 상체만 채찍처럼 휙! 휘둘러 던지세요.",
        "vision_title": "🛰️ Future Mission: 인류의 모든 움직임을 데이터화하다", "vision_desc": "본 시스템은 육상 15개 전 종목의 생체역학을 하나의 AI로 통합한 '파운데이션 모델'입니다.",
        "f_title": "🧪 ATHLETICS 연구소", "f_desc": "당신의 의견이 더 똑똑한 AI 코치를 만듭니다."
    },
    "🇺🇸 English": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Global Track & Field Biomechanics System", "toss": "Powered by ATHLETICS AI",
        "s_head": "⚙️ System Config", "s_lang": "🌐 UI Language", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark Target", "s_up": "Select Video (Max 10s)", "s_btn": "🚀 Run AI Analysis", "r_title": "🔬 Biometric Diagnostic Report",
        "img_title": "📸 Vision AI Skeletal Tracking",
        "tab_pro": "🎓 Pro Biomechanics", "tab_kids": "🎈 Kids Play & Drill",
        "c_sprint_pro": "<b>[Sprint Kinematics]</b> Knee extension at {avg_angle}° shows {gap:.1f}° early recovery. SSC energy is leaking.<br><b>[Drill]</b> Depth jumps for maximum ankle stiffness.",
        "c_sprint_kids": "<b>[Hot Lava Game]</b> Pretend the ground is hot lava! Touch it quickly with your toes and blast off like a rocket!",
        "c_mara_pro": "<b>[Marathon Efficiency]</b> Lack of triple extension causes a {gap:.1f}° deviation. Vertical GRF dispersion noted.<br><b>[Drill]</b> Iliopsoas stretching & Single-leg deadlifts.",
        "c_mara_kids": "<b>[Water Cup Challenge]</b> Imagine a full cup of water on your head! Don't bounce up and down; glide smoothly like a ninja.",
        "c_jump_pro": "<b>[Jump Mechanics]</b> Insufficient COM drop in the penultimate step.<br><b>[Drill]</b> Hinge control and upward arm drive synchronization.",
        "c_jump_kids": "<b>[Frog Jump]</b> Bend your knees a bit more on the last step, stomp hard, and throw your arms up like Superman!",
        "c_throw_pro": "<b>[Throw Mechanics]</b> Weak blocking leg breaks the kinetic chain.<br><b>[Drill]</b> Bracing drills and thoracic mobility for X-Factor.",
        "c_throw_kids": "<b>[Human Catapult]</b> Play Freeze-Throw! Plant your front foot, yell 'Freeze!', and whip your upper body like a catapult.",
        "vision_title": "🛰️ Future Mission: Digitizing Human Movement", "vision_desc": "A Foundation Model integrating biomechanics for all 15 Track & Field events.",
        "f_title": "🧪 ATHLETICS AI Lab", "f_desc": "Your feedback builds a smarter AI Coach."
    },
    "🇯🇵 日本語": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "グローバル陸上バイオメカニクスシステム", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ 設定", "s_lang": "🌐 言語", "s_cat": "🏟️ カテゴリ", "s_sport": "🏃‍♂️ 種目", "s_data": "📊 比較データ", "s_up": "動画を選択", "s_btn": "🚀 AI分析を実行", "r_title": "🔬 バイオメカニクス診断レポート",
        "img_title": "📸 AI骨格トラッキング",
        "tab_pro": "🎓 プロフェッショナル分析", "tab_kids": "🎈 キッズ向け練習法",
        "c_sprint_pro": "<b>[スプリント]</b> 膝の伸展が{avg_angle}°で、{gap:.1f}°の早期回収が見られます。SSCのエネルギーロス。<br><b>[練習]</b> デプスジャンプで足首の剛性を強化。",
        "c_sprint_kids": "<b>[マグマジャンプ]</b> 床が熱いマグマだと思って、つま先で一瞬だけ触れてロケットみたいに飛び出そう！",
        "c_mara_pro": "<b>[マラソン]</b> 完全伸展不足（{gap:.1f}°の偏差）。GRFが垂直に分散。<br><b>[練習]</b> 腸腰筋ストレッチと体幹安定化トレーニング。",
        "c_mara_kids": "<b>[忍者走り]</b> 頭の上に水が入ったコップを乗せていると想像して！上下に揺れずに、忍者のように静かに走ろう。",
        "c_jump_pro": "<b>[跳躍]</b> 踏切前の重心降下が不十分です。<br><b>[練習]</b> 踏切前の沈み込みと腕の振り上げの連動トレーニング。",
        "c_jump_kids": "<b>[スーパーマンジャンプ]</b> 最後の1歩でカエルみたいに膝を曲げて、バーン！と踏み込んでバンザイして飛ぼう！",
        "c_throw_pro": "<b>[投擲]</b> ブロッキングの崩れによりキネティックチェーンが切断。<br><b>[練習]</b> ブレーシングと胸椎の可動域拡張トレーニング。",
        "c_throw_kids": "<b>[人間投石機]</b> 投げる瞬間に前足を『ピタッ』と止めて、上半身だけムチのように振って投げよう！",
        "vision_title": "🛰️ Future Mission: 人類の動きをデータ化", "vision_desc": "陸上15種目を統合するAIファウンデーションモデルです。",
        "f_title": "🧪 AI研究所", "f_desc": "あなたのフィードバックがAIを賢くします。"
    },
    "🇨🇳 中文": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "全球田径生物力学教育系统", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ 系统设置", "s_lang": "🌐 语言", "s_cat": "🏟️ 类别", "s_sport": "🏃‍♂️ 项目", "s_data": "📊 对比基准", "s_up": "选择视频 (最多10秒)", "s_btn": "🚀 运行 AI 分析", "r_title": "🔬 生物力学诊断报告",
        "img_title": "📸 视觉 AI 骨骼追踪",
        "tab_pro": "🎓 专家级分析", "tab_kids": "🎈 儿童训练法",
        "c_sprint_pro": "<b>[短跑力学]</b> 膝关节伸展仅为 {avg_angle}°，存在 {gap:.1f}° 的提前回收。SSC 能量正在流失。<br><b>[训练]</b> 通过深度跳跃最大化踝关节刚度。",
        "c_sprint_kids": "<b>[岩浆跳跃]</b> 想象地板是滚烫的岩浆！只用脚尖轻轻点地，像火箭一样冲出去！",
        "c_mara_pro": "<b>[马拉松效率]</b> 未实现完全伸展，存在 {gap:.1f}° 偏差。地面反作用力垂直分散。<br><b>[训练]</b> 髂腰肌动态拉伸和单腿硬拉。",
        "c_mara_kids": "<b>[头顶水杯]</b> 想象头上顶着一杯水！不要上下颠簸，像忍者一样平稳地奔跑。",
        "c_jump_pro": "<b>[跳跃力学]</b> 倒数第二步重心下降不足。<br><b>[训练]</b> 练习重心下降与手臂上摆的同步。",
        "c_jump_kids": "<b>[青蛙跳]</b> 在最后一步像青蛙一样稍微弯曲膝盖，用力踩地，举起双手像超人一样飞起来！",
        "c_throw_pro": "<b>[投掷力学]</b> 前腿制动不足破坏了动力链。<br><b>[训练]</b> 制动训练和增加胸椎活动度。",
        "c_throw_kids": "<b>[人体投石机]</b> 玩“木头人”游戏！前脚落地时喊“停！”，然后像鞭子一样挥动上半身投掷。",
        "vision_title": "🛰️ Future Mission: 数字化人类运动", "vision_desc": "整合15个田径项目的 AI 基础模型。",
        "f_title": "🧪 AI 实验室", "f_desc": "您的反馈将建立更智能的 AI 教练。"
    },
    "🇪🇸 Español": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Sistema Global de Biomecánica", "toss": "Toss ID: ATHLETICS AI",
        "s_head": "⚙️ Configuración", "s_lang": "🌐 Idioma", "s_cat": "🏟️ Categoría", "s_sport": "🏃‍♂️ Evento", "s_data": "📊 Referencia", "s_up": "Subir Video", "s_btn": "🚀 Ejecutar Análisis", "r_title": "🔬 Reporte Biomecánico",
        "img_title": "📸 Seguimiento de Esqueleto AI",
        "tab_pro": "🎓 Análisis Profesional", "tab_kids": "🎈 Entrenamiento para Niños",
        "c_sprint_pro": "<b>[Mecánica de Sprint]</b> Extensión de rodilla a {avg_angle}°. Recuperación temprana de {gap:.1f}°. Fuga de energía SSC.<br><b>[Ejercicio]</b> Saltos de profundidad para rigidez del tobillo.",
        "c_sprint_kids": "<b>[Juego de Lava]</b> ¡Imagina que el suelo es lava! Toca rápido con la punta del pie y despega como un cohete.",
        "c_mara_pro": "<b>[Eficiencia Maratón]</b> Desviación de {gap:.1f}° por falta de triple extensión. Dispersión vertical de GRF.<br><b>[Ejercicio]</b> Estiramiento de psoas y peso muerto a una pierna.",
        "c_mara_kids": "<b>[Vaso de Agua]</b> ¡Imagina un vaso de agua en tu cabeza! No rebotes, corre suave como un ninja.",
        "c_jump_pro": "<b>[Salto]</b> Caída insuficiente del centro de masa en el penúltimo paso.<br><b>[Ejercicio]</b> Sincronización de caída y balanceo de brazos.",
        "c_jump_kids": "<b>[Salto de Rana]</b> ¡Dobla las rodillas en el último paso, pisa fuerte y levanta los brazos como Superman!",
        "c_throw_pro": "<b>[Lanzamiento]</b> El bloqueo débil rompe la cadena cinética.<br><b>[Ejercicio]</b> Ejercicios de bloqueo y movilidad torácica.",
        "c_throw_kids": "<b>[Catapulta]</b> ¡Planta tu pie delantero, quédate congelado y lanza la parte superior de tu cuerpo como un látigo!",
        "vision_title": "🛰️ Misión Futura: Digitalizar el Movimiento", "vision_desc": "Modelo fundacional que integra la biomecánica de 15 eventos de atletismo.",
        "f_title": "🧪 Laboratorio AI", "f_desc": "Tus comentarios construyen un entrenador AI más inteligente."
    }
}

# 3. 카테고리 및 데이터베이스 (표준화 유지)
categories = {
    "Track (달리기/허들)": {
        "metrics": ['Knee Ext.', 'GCT', 'Oscillation', 'Pelvic Bal.', 'Arm Sync'],
        "sports": ["100m Sprint", "400m Sprint", "Marathon", "Hurdle", "Race Walking"]
    },
    "Jump (도약)": {
        "metrics": ['Take-off', 'COM Drop', 'Approach Vel.', 'Flight Time', 'Landing'],
        "sports": ["Long Jump", "Triple Jump", "High Jump", "Pole Vault"]
    },
    "Throw (투척)": {
        "metrics": ['Release Angle', 'Velocity', 'Blocking', 'Trunk Twist', 'Shoulder'],
        "sports": ["Javelin Throw", "Shot Put"]
    }
}

benchmarks = {
    "🌍 World Record": {"angle": 175.5, "radar": [99, 98, 97, 99, 98], "color": "#000000"},
    "🥇 Olympic Gold": {"angle": 172.0, "radar": [96, 95, 96, 95, 97], "color": "#F1BF00"},
    "🇰🇷 Korea Elite": {"angle": 165.5, "radar": [88, 90, 85, 88, 90], "color": "#CD2E3A"},
    "🌐 Global Amateur": {"angle": 150.0, "radar": [60, 65, 55, 60, 70], "color": "#888888"}
}

# 4. CSS 세팅
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

# 5. 사이드바 (언어 선택 적용)
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language", list(ui_langs.keys()))
    t = ui_langs[selected_lang]
    st.markdown("---")
    
    selected_cat = st.selectbox(t['s_cat'], list(categories.keys()))
    selected_sport = st.selectbox(t['s_sport'], categories[selected_cat]["sports"])
    selected_bench = st.selectbox(t['s_data'], list(benchmarks.keys()))
    b_data = benchmarks[selected_bench]
    
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
    with st.spinner('Translating & Generating AI Coaching...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]; avg_angle = 155.9 
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
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.markdown(f"""<div class="data-card" style="margin-top: 25px; border-top: 4px solid #F9AB00;"><h5 style="color: #202124; margin: 0;">{t['img_title']}</h5></div>""", unsafe_allow_html=True)
        x_my = -np.sin(np.radians(180-avg_angle)); y_my = -np.cos(np.radians(180-avg_angle))
        x_tg = -np.sin(np.radians(180-target_angle)); y_tg = -np.cos(np.radians(180-target_angle))
        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(x=[0, 0], y=[1, 0], mode='lines+markers', line=dict(color='white', width=8), name='Axis'))
        fig_ov.add_trace(go.Scatter(x=[0, x_my], y=[0, y_my], mode='lines+markers', line=dict(color='#D93025', width=8), name=f'My ({avg_angle}°)'))
        fig_ov.add_trace(go.Scatter(x=[0, x_tg], y=[0, y_tg], mode='lines', line=dict(color='#64FFDA', width=4, dash='dash'), name=f'Standard ({target_angle}°)'))
        fig_ov.update_layout(plot_bgcolor='#0A192F', paper_bgcolor='#0A192F', font=dict(color='white'), xaxis=dict(visible=False, range=[-0.5, 0.5]), yaxis=dict(visible=False, range=[-1.2, 1.2]), margin=dict(l=20, r=20, t=20, b=20), height=480, showlegend=True)
        st.plotly_chart(fig_ov, use_container_width=True)

    with col4:
        st.markdown('<div class="coaching-box" style="margin-top: 25px;">', unsafe_allow_html=True)
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        
        # 언어팩을 기반으로 한 다국어 동적 코칭 출력
        if "Sprint" in selected_sport:
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif "Marathon" in selected_sport:
            with tab_pro: st.markdown(t['c_mara_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        elif "Jump" in selected_cat:
            with tab_pro: st.markdown(t['c_jump_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_jump_kids'], unsafe_allow_html=True)
        elif "Throw" in selected_cat:
            with tab_pro: st.markdown(t['c_throw_pro'].format(avg_angle=avg_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_throw_kids'], unsafe_allow_html=True)
        else:
            with tab_pro: st.markdown("Analyzing...")
            with tab_kids: st.markdown("Have fun!")
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown(f"""<div class="vision-card"><h3 style="color: #1A73E8;">{t['vision_title']}</h3><p>{t['vision_desc']}</p></div>""", unsafe_allow_html=True)

# 8. 구글 엑셀 연동
st.markdown("---")
with st.form(key='athletics_ai_form', clear_on_submit=True):
    user_comment = st.text_area(t['f_title'], placeholder=t['f_desc'])
    submit_button = st.form_submit_button(label="Submit", type="primary")
    if submit_button and user_comment:
        try:
            url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
            data = {"entry.503694872": user_comment}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data)
            urllib.request.urlopen(req)
            st.balloons(); st.success(t['f_success'])
        except: st.error("Error")
