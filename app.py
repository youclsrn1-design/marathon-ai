import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (7대 언어: KO, EN, JP, CN, ES, HI, FR)
# 전문가(4단계 논리) + 어린이(현지어 & Easy English + 지도자 가이드) 보강
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "인류의 모든 움직임을 데이터화하는 글로벌 육상 생체역학 파운데이션",
        "s_head": "⚙️ 시스템 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 벤치마크 (국가별)", "s_up": "영상 업로드 (10초)", "s_btn": "🚀 AI 딥 코칭 실행", "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 대조", "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 영어 체육 (Kids)",
        "c_sprint_pro": "🎯 <b>[칭찬 및 강점]</b> 매우 폭발적인 초기 가속력을 보유하고 있으며, 지면을 박차고 나가는 킥의 각도가 세계적인 선수들과 매우 유사합니다.<br>⚖️ <b>[장단점 분석]</b> 상체의 안정적인 전방 기울기는 훌륭하나(장점), 높은 주폭을 유지하기 위한 무릎 회수 속도가 조금 느린 편입니다(단점).<br>🚨 <b>[문제 진단]</b> 현재 무릎 신전 각도는 <b>{avg_angle}°</b>로 목표치인 {target_angle}° 대비 <b>{gap:.1f}°의 오차</b>가 발생하고 있습니다. 이는 지면 접촉 시 탄성 에너지를 충분히 활용하지 못하고 지면에 에너지를 버리고 있음을 의미합니다.<br>💡 <b>[해결 및 훈련법]</b> 1단계: 뎁스 점프를 통해 발목의 강성을 키워 지면 접촉 시간을 0.1초 단축하세요. 2단계: 전족부(발 앞꿈치)로 트랙을 수직으로 강하게 타격하는 리듬 훈련을 병행하십시오.",
        "c_sprint_kids": "🌟 <b>[Great Job! 최고예요]</b> You run like a rocket! (우리 친구, 정말 로켓처럼 빠르게 달리네요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good focus, but keep your back straight! (집중하는 모습은 정말 좋은데, 허리를 조금만 더 곧게 펴볼까요?)<br>🔥 <b>[Play: Hot Lava Game 용암 놀이]</b> The ground is hot lava! Touch it quickly with your toes! (바닥이 아주 뜨거운 용암이에요! 발바닥 전체가 아니라 앞꿈치로만 '앗 뜨거!' 하면서 빠르게 땅을 치고 날아가 보세요!)<br>👨‍🏫 <b>[지도자 가이드]</b> 아이가 달릴 때 뒤꿈치가 먼저 닿지 않도록 주의 깊게 관찰해 주세요. '소리 없이 가볍게 뛰기' 미션을 주면 자연스럽게 앞꿈치를 사용하게 됩니다.",
        "vision_title": "🛰️ Future Mission: 글로벌 표준 데이터화", "vision_desc": "이 시스템은 전 세계 모든 육상 선수의 데이터를 수집하여 구글 AR 스마트 안경에 실시간 역학 정보를 투사하기 위한 파운데이션 모델입니다.", "f_title": "🧪 AI 연구소", "f_desc": "여러분의 소중한 피드백이 AI 코치를 더 똑똑하게 만듭니다."
    },
    "🇺🇸 English": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Global Biomechanics Foundation Digitizing Human Movement",
        "s_head": "⚙️ Settings", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Coaching", "r_title": "🔬 AI Biomechanics Report", "img_title": "📸 Vision AI Skeletal Tracking", "tab_pro": "🎓 Pro Biomechanics", "tab_kids": "🎈 Easy English Kids",
        "c_sprint_pro": "🎯 <b>[Praise & Strengths]</b> You demonstrate explosive initial acceleration and excellent torso lean.<br>⚖️ <b>[Analysis]</b> While upper body stability is top-notch (Pro), lower limb ground force is slightly dissipated (Con).<br>🚨 <b>[Diagnosis]</b> Knee extension at <b>{avg_angle}°</b> shows a <b>{gap:.1f}° early recovery</b>. SSC energy is leaking during ground contact.<br>💡 <b>[Solution]</b> Step 1: Maximize ankle stiffness through depth jumps. Step 2: Implement vertical forefoot striking drills to minimize ground contact time.",
        "c_sprint_kids": "🌟 <b>[Great Job!]</b> You run like a rocket!<br>🔍 <b>[Pros & Cons]</b> Great focus, but try to look straight ahead!<br>🔥 <b>[Play: Hot Lava Game]</b> The ground is hot lava! Touch it quickly with your toes and blast off!<br>👨‍🏫 <b>[Coach Guide]</b> Watch for heel-striking. Encourage children to 'run quietly' to promote forefoot usage naturally.",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Projecting global athletics data into AR glasses for real-time performance feedback.", "f_title": "🧪 AI Lab", "f_desc": "Your feedback builds a smarter AI."
    },
    "🇯🇵 日本語": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "人類のすべての動きをデータ化するバイオメカニクスAI",
        "s_head": "⚙️ 設定", "s_cat": "🏟️ カテゴリ", "s_sport": "🏃‍♂️ 種目", "s_data": "📊 比較対象", "s_up": "動画を選択", "s_btn": "🚀 AI分析を実行", "r_title": "🔬 AI診断レポート", "img_title": "📸 AI骨格トラッキング", "tab_pro": "🎓 プロフェッショナル分析", "tab_kids": "🎈 子供向け英語体育 (Kids)",
        "c_sprint_pro": "🎯 <b>[称賛と強み]</b> 素晴らしい爆発的な初期加速と、安定した前傾姿勢を維持しています。<br>⚖️ <b>[分析]</b> 腕の振りのバランスは非常に良いですが（長所）、地面を蹴り出す推進力がやや不足しています（短所）。<br>🚨 <b>[課題診断]</b> 膝の伸展が <b>{avg_angle}°</b> で、目標値に対して <b>{gap:.1f}°の早期回収</b>が見られます。エネルギーが地面に逃げています。<br>💡 <b>[解決策]</b> ステップ1：デプスジャンプで足首の剛性を高めます。ステップ2：フォアフット（前足部）で地面を叩くリズムを意識してください。",
        "c_sprint_kids": "🌟 <b>[Great Job! すごい！]</b> You run like a rocket! (ロケットみたいに速いね！)<br>🔍 <b>[Pros & Cons]</b> Good arms, but keep your back straight! (腕はいいけど、背中を真っ直ぐにしよう！)<br>🔥 <b>[Play: マグマ遊び]</b> The ground is hot lava! Touch it quickly! (地面は熱いマグマだよ！つま先で素早くタッチして飛び出そう！)<br>👨‍🏫 <b>[指導者ガイド]</b> かかとから接地していないか確認してください。「静かに走る」練習をさせると、自然とつま先を使えるようになります。",
        "vision_title": "🛰️ 未来のミッション", "vision_desc": "世界の陸上データをARグラスに投影するプラットフォーム。", "f_title": "🧪 AI研究所", "f_desc": "フィードバックをお願いします。"
    },
    "🇨🇳 中文": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "全球田径生物力学基础模型",
        "s_head": "⚙️ 系统设置", "s_cat": "🏟️ 类别", "s_sport": "🏃‍♂️ 项目", "s_data": "📊 对比基准", "s_up": "上传视频", "s_btn": "🚀 运行 AI 诊断", "r_title": "🔬 AI 生物力学报告", "img_title": "📸 视觉 AI 骨骼追踪", "tab_pro": "🎓 专家级分析", "tab_kids": "🎈 儿童英语体育 (Kids)",
        "c_sprint_pro": "🎯 <b>[优点与称赞]</b> 具有极佳的爆发性初始加速，身体前倾角度非常专业。<br>⚖️ <b>[优缺点分析]</b> 手臂摆动非常平衡（优），但下肢对地面的反作用力利用不足（缺）。<br>🚨 <b>[问题诊断]</b> 膝关节伸展为 <b>{avg_angle}°</b>，存在 <b>{gap:.1f}° 的提前回收</b>。SSC弹性效率正在流失。<br>💡 <b>[训练方案]</b> 第一步：通过深度跳跃增加踝关节刚度。第二步：练习用前脚掌垂直击打地面，缩短触地时间。",
        "c_sprint_kids": "🌟 <b>[Great Job! 太棒了]</b> You run like a rocket! (你跑得像火箭一样快！)<br>🔍 <b>[Pros & Cons]</b> Good focus, but bend knees less! (注意力很集中，但膝盖再伸直一点点！)<br>🔥 <b>[Play: 岩浆游戏]</b> The ground is hot lava! Touch it quickly! (地面是滚烫的岩浆！快用脚尖点地飞起来！)<br>👨‍🏫 <b>[指导指南]</b> 观察孩子是否用脚跟落地。通过“像猫一样轻声奔跑”的指令，引导孩子使用前脚掌。",
        "vision_title": "🛰️ 未来使命", "vision_desc": "将全球田径数据实时投射到 AR 眼镜的平台。", "f_title": "🧪 AI 实验室", "f_desc": "您的反馈非常重要。"
    },
    "🇪🇸 Español": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Fundación global de biomecánica del movimiento",
        "s_head": "⚙️ Ajustes", "s_cat": "🏟️ Categoría", "s_sport": "🏃‍♂️ Evento", "s_data": "📊 Referencia", "s_up": "Subir Video", "s_btn": "🚀 Ejecutar AI", "r_title": "🔬 Reporte Biomecánico AI", "img_title": "📸 Seguimiento de Esqueleto", "tab_pro": "🎓 Análisis Pro", "tab_kids": "🎈 Inglés Fácil (Kids)",
        "c_sprint_pro": "🎯 <b>[Fortalezas]</b> Excelente aceleración inicial y postura aerodinámica.<br>⚖️ <b>[Análisis]</b> Buen braceo (Pro), pero el empuje contra el suelo es débil (Con).<br>🚨 <b>[Diagnóstico]</b> Extensión a <b>{avg_angle}°</b>. <b>{gap:.1f}° de recuperación temprana</b>. Pérdida de energía elástica.<br>💡 <b>[Solución]</b> Paso 1: Saltos de profundidad para rigidez del tobillo. Paso 2: Ejercicios de impacto con el antepié para reducir el tiempo de contacto.",
        "c_sprint_kids": "🌟 <b>[Great Job! ¡Genial!]</b> You run like a rocket! (¡Corres como un cohete!)<br>🔍 <b>[Pros & Cons]</b> Good energy, but look straight! (¡Buena energía, pero mira al frente!)<br>🔥 <b>[Play: El suelo es lava]</b> The ground is hot lava! Touch it quickly! (¡El suelo es lava! ¡Tócalo rápido con las puntas!)<br>👨‍🏫 <b>[Guía del entrenador]</b> Asegúrese de que no pisen con el talón. El juego de 'correr como un ninja' ayuda a usar el antepié.",
        "vision_title": "🛰️ Misión Futura", "vision_desc": "Datos biomecánicos proyectados en gafas AR inteligentes.", "f_title": "🧪 Laboratorio AI", "f_desc": "Tu opinión nos hace mejores."
    },
    "🇮🇳 हिन्दी (Hindi)": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "ग्लोबल बायोमैकेनिक्स सिस्टम",
        "s_head": "⚙️ सेटिंग्स", "s_cat": "🏟️ श्रेणी", "s_sport": "🏃‍♂️ खेल", "s_data": "📊 बेंचमार्क", "s_up": "वीडियो अपलोड करें", "s_btn": "🚀 AI विश्लेषण", "r_title": "🔬 AI बायोमैकेनिक्स रिपोर्ट", "img_title": "📸 AI कंकाल ट्रैकिंग", "tab_pro": "🎓 पेशेवर विश्लेषण", "tab_kids": "🎈 बच्चों के लिए खेल (Kids)",
        "c_sprint_pro": "🎯 <b>[प्रशंसा]</b> बहुत बढ़िया त्वरण और शारीरिक संतुलन।<br>⚖️ <b>[विश्लेषण]</b> हाथों का तालमेल अच्छा है, लेकिन पैरों की शक्ति जमीन पर कम हो रही है।<br>🚨 <b>[निदान]</b> घुटने का विस्तार <b>{avg_angle}°</b> है, जो मानक से <b>{gap:.1f}° कम</b> है। ऊर्जा का रिसाव हो रहा है।<br>💡 <b>[समाधान]</b> चरण 1: टखनों की शक्ति बढ़ाने के लिए जंप अभ्यास करें। चरण 2: जमीन पर पैर रखने का समय कम करने के लिए पंजे का उपयोग करें।",
        "c_sprint_kids": "🌟 <b>[Great Job! बहुत बढ़िया!]</b> You run like a rocket! (तुम रॉकेट की तरह दौड़ते हो!)<br>🔍 <b>[Pros & Cons]</b> Great arms, but look ahead! (हाथ अच्छे हैं, सामने देखो!)<br>🔥 <b>[Play: गर्म लावा]</b> The ground is hot lava! Touch it quickly! (जमीन लावा है! जल्दी से पैर छुओ और उड़ जाओ!)<br>👨‍🏫 <b>[कोच गाइड]</b> ध्यान दें कि बच्चे एड़ी के बल न दौड़ें। उन्हें 'बिना आवाज किए दौड़ने' के लिए कहें।",
        "vision_title": "🛰️ फ्यूचर मिशन", "vision_desc": "एआर चश्मे में वैश्विक डेटा पेश करना।", "f_title": "🧪 AI लैब", "f_desc": "अपनी प्रतिक्रिया दें।"
    },
    "🇫🇷 Français": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "La Fondation Biomécanique Mondiale",
        "s_head": "⚙️ Paramètres", "s_cat": "🏟️ Catégorie", "s_sport": "🏃‍♂️ Événement", "s_data": "📊 Référence", "s_up": "Télécharger Vidéo", "s_btn": "🚀 Lancer l'AI", "r_title": "🔬 Rapport Biomécanique AI", "img_title": "📸 Suivi Squelettique AI", "tab_pro": "🎓 Diagnostic Pro", "tab_kids": "🎈 Kids (Anglais Facile)",
        "c_sprint_pro": "🎯 <b>[Points forts]</b> Accélération initiale explosive et excellente inclinaison du tronc.<br>⚖️ <b>[Analyse]</b> Bon équilibre des bras (Pro), mais force d'appui insuffisante (Con).<br>🚨 <b>[Diagnostic]</b> Extension à <b>{avg_angle}°</b>. <b>{gap:.1f}° de récupération précoce</b>. Perte d'énergie SSC.<br>💡 <b>[Solution]</b> 1. Sauts profonds (stabilité cheville). 2. Exercices d'appui avant-pied pour réduire le temps de contact au sol.",
        "c_sprint_kids": "🌟 <b>[Great Job! Super !]</b> You run like a rocket! (Tu cours comme une fusée !)<br>🔍 <b>[Pros & Cons]</b> Good arms, but keep your back straight! (Bons bras, mais tiens-toi droit !)<br>🔥 <b>[Play: Le sol est de la lave]</b> The ground is hot lava! Touch it quickly! (Le sol est de la lave ! Touche-le vite avec tes orteils !)<br>👨‍🏫 <b>[Guide Coach]</b> Vérifiez que l'enfant ne pose pas le talon en premier. Donnez-lui le défi de 'courir sans bruit'.",
        "vision_title": "🛰️ Mission Future", "vision_desc": "Projection de données mondiales dans des lunettes AR pour un feedback en temps réel.", "f_title": "🧪 Laboratoire AI", "f_desc": "Vos retours nous aident à progresser."
    }
}

# 3. 🏟️ 육상 전 종목 카테고리 & 벤치마크 DB (미국, 일본, 중국, 인도, 프랑스 등)
categories = {
    "Track (트랙/달리기)": {
        "metrics": ['무릎 신전', '지면접촉시간', '수직진폭', '골반 밸런스', '상하체 동기화'],
        "sports": ["100m 단거리 (Sprint)", "400m 스프린트", "마라톤 (Marathon)", "100m/110m 허들", "경보 (Race Walking)"]
    },
    "Jump (도약/뛰기)": {
        "metrics": ['도약 무릎각', '무게중심 강하', '진입 속도', '체공 시간', '착지 안정성'],
        "sports": ["멀리뛰기 (Long Jump)", "세단뛰기 (Triple Jump)", "높이뛰기 (High Jump)", "장대높이뛰기 (Pole Vault)"]
    },
    "Throw (투척/던지기)": {
        "metrics": ['릴리스 각도', '투척 속도', '앞발 블록킹', '몸통 비틀림', '어깨 회전축'],
        "sports": ["창던지기 (Javelin)", "포환던지기 (Shot Put)"]
    }
}

benchmark_db = {
    "Sprint": {"🌍 World Record": {"angle": 172.5, "radar": [99, 99, 90, 98, 99], "color": "#000000"}, "🇯🇲 Jamaica": {"angle": 171.0, "radar": [97, 98, 88, 97, 98], "color": "#009B3A"}, "🇺🇸 USA": {"angle": 170.5, "radar": [96, 96, 89, 95, 96], "color": "#3C3B6E"}, "🇯🇵 Japan": {"angle": 169.5, "radar": [95, 96, 88, 94, 95], "color": "#BC002D"}, "🇨🇳 China": {"angle": 169.0, "radar": [94, 95, 87, 93, 94], "color": "#EE1C25"}, "🇮🇳 India": {"angle": 168.0, "radar": [90, 92, 85, 90, 92], "color": "#FF9933"}},
    "Distance": {"🌍 World Record": {"angle": 168.5, "radar": [98, 97, 96, 99, 98], "color": "#000000"}, "🇰🇪 Kenya": {"angle": 167.5, "radar": [96, 95, 94, 96, 97], "color": "#009E60"}, "🇯🇵 Japan": {"angle": 165.5, "radar": [92, 94, 88, 92, 95], "color": "#BC002D"}, "🇫🇷 France": {"angle": 164.5, "radar": [90, 92, 86, 91, 93], "color": "#002395"}},
    "Walk": {"🌍 World Record": {"angle": 180.0, "radar": [99, 95, 98, 99, 97], "color": "#000000"}, "🇨🇳 China": {"angle": 179.5, "radar": [98, 94, 97, 98, 96], "color": "#EE1C25"}, "🇪🇸 Spain": {"angle": 178.8, "radar": [96, 92, 95, 96, 94], "color": "#F1BF00"}},
    "Jump": {"🌍 World Record": {"angle": 178.0, "radar": [99, 98, 99, 96, 98], "color": "#000000"}, "🇺🇸 USA": {"angle": 176.0, "radar": [97, 95, 96, 94, 95], "color": "#3C3B6E"}, "🇨🇺 Cuba": {"angle": 177.5, "radar": [96, 94, 98, 93, 94], "color": "#CB1515"}},
    "Throw": {"🌍 World Record": {"angle": 175.0, "radar": [98, 99, 99, 97, 98], "color": "#000000"}, "🇮🇳 India (Neeraj)": {"angle": 174.0, "radar": [96, 97, 96, 94, 95], "color": "#FF9933"}, "🇩🇪 Germany": {"angle": 174.5, "radar": [96, 98, 97, 95, 96], "color": "#FFCE00"}}
}

# 4. 고급 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .hero-section { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 60px 20px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .hero-title { color: #64FFDA; font-size: 3.8em; font-weight: 900; letter-spacing: 1px; margin-bottom: 10px; }
    .hero-sub { color: #CCD6F6; font-size: 1.3em; font-weight: 400; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 35px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.7; }
    </style>
    """, unsafe_allow_html=True)

# 5. 사이드바 
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

# 🚀 Hero Section (후원 버튼 제거 후 웅장함 극대화)
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t['title']}</h1>
        <p class="hero-sub">{t['sub']}</p>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('AI Biomechanics Foundation Engine Analyzing...'):
        score = 78; my_stats = [75, 68, 85, 70, 65]
        if b_group_name == "Sprint": avg_angle = 158.5
        elif b_group_name == "Distance": avg_angle = 155.9
        elif b_group_name == "Walk": avg_angle = 172.0
        elif b_group_name == "Jump": avg_angle = 162.5
        elif b_group_name == "Throw": avg_angle = 158.0
        target_angle = b_data['angle']; gap = target_angle - avg_angle
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
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=300, margin=dict(l=60, r=60, t=30, b=20), paper_bgcolor="rgba(0,0,0,0)")
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
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        if b_group_name == "Sprint":
            with tab_pro: st.markdown(t['c_sprint_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_sprint_kids'], unsafe_allow_html=True)
        elif b_group_name == "Distance":
            with tab_pro: st.markdown(t['c_mara_pro'].format(gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_mara_kids'], unsafe_allow_html=True)
        else:
            with tab_pro: st.markdown(t['c_general_pro'].format(avg_angle=avg_angle, target_angle=target_angle, gap=gap), unsafe_allow_html=True)
            with tab_kids: st.markdown(t['c_general_kids'], unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 7. 비전 섹션
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""<div style="background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 40px; border-radius: 12px;"><h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3><p style="font-size: 1.2em; color: #3C4043;">{t['vision_desc']}</p></div>""", unsafe_allow_html=True)

# 8. 구글 엑셀 연동
st.markdown("---")
with st.form(key='athletics_ai_form', clear_on_submit=True):
    user_comment = st.text_area(t['f_title'], placeholder=t['f_desc'])
    submit_button = st.form_submit_button(label="Submit Feedback", type="primary")
    if submit_button and user_comment:
        try:
            url = "https://docs.google.com/forms/d/e/1FAIpQLScq5MZNK2TmD7TknmRBnLqm7j0ci9FQY4GwBD4NmZTT8t0Lzg/formResponse"
            data = {"entry.503694872": user_comment}
            encoded_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data=encoded_data)
            urllib.request.urlopen(req)
            st.balloons(); st.success(t['f_success'])
        except: st.error("Error")
