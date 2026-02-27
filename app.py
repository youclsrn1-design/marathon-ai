import streamlit as st
import numpy as np
import plotly.graph_objects as go
import urllib.parse
import urllib.request

# 1. 시스템 기본 설정
st.set_page_config(page_title="Global Athletics AI | Foundation", layout="wide", initial_sidebar_state="expanded")

# 2. 글로벌 UI 언어팩 (7대 언어 완벽 지원 및 코칭 로직 강화)
ui_langs = {
    "🇰🇷 한국어": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "인류의 모든 움직임을 데이터화하는 육상 생체역학 파운데이션",
        "s_head": "⚙️ 시스템 설정", "s_cat": "🏟️ 카테고리", "s_sport": "🏃‍♂️ 세부 종목", "s_data": "📊 벤치마크 (국가별)", "s_up": "영상 업로드 (10초)", "s_btn": "🚀 AI 딥 코칭 실행", "r_title": "🔬 AI 생체역학 정밀 진단 리포트", "img_title": "📸 비전 AI 관절 궤적 대조", "tab_pro": "🎓 전문가 심화 학습", "tab_kids": "🎈 어린이 영어 체육 (Kids)", "toss": "💙 Toss 후원: ATHLETICS AI",
        
        "c_sprint_pro": "🎯 <b>[칭찬 및 강점]</b> 훌륭한 초기 가속과 안정적인 상체 기울기입니다.<br>⚖️ <b>[장단점 분석]</b> 팔치기 밸런스는 좋으나, 하체 지면 발진력이 부족합니다.<br>🚨 <b>[문제 진단]</b> 무릎 신전 <b>{avg_angle}°</b> (목표 {target_angle}°). <b>{gap:.1f}° 조기 회수</b>로 SSC 탄성 에너지 누수 발생.<br>💡 <b>[해결 및 훈련법]</b> 1. 뎁스 점프(발목 강성 극대화) 2. 전족부 타격 훈련 3. 팔-다리 폭발적 동기화",
        "c_sprint_kids": "🌟 <b>[Great Job! 최고예요]</b> You run so fast! (정말 빨리 달리네요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good arms, but bend knees less! (팔은 멋진데, 무릎을 덜 굽혀봐요!)<br>🔥 <b>[Hot Lava Game 용암 놀이]</b> The ground is hot lava! Touch it quickly with your toes! (바닥이 뜨거운 용암이에요! 앞꿈치로 빨리 터치하고 날아가요!)",
        
        "c_mara_pro": "🎯 <b>[칭찬 및 강점]</b> 일정한 호흡과 흔들림 없는 상체 밸런스가 뛰어납니다.<br>⚖️ <b>[장단점 분석]</b> 지구력은 좋으나, 보폭당 에너지 효율이 떨어집니다.<br>🚨 <b>[문제 진단]</b> <b>{gap:.1f}° 편차</b>. 골반 드롭으로 지면반발력이 수직 분산되어 햄스트링 과부하 유발.<br>💡 <b>[해결 및 훈련법]</b> 1. 장요근 스트레칭 2. 싱글 레그 데드리프트 3. 미드풋 스트라이크",
        "c_mara_kids": "🌟 <b>[Great Job! 최고예요]</b> Amazing energy! (에너지가 넘치네요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good breathing, but don't bounce! (숨쉬기는 좋은데, 콩콩 뛰지 마세요!)<br>💧 <b>[Water Cup Game 물컵 놀이]</b> Imagine a water cup on your head! Glide like a ninja! (머리 위에 물컵이 있어요! 닌자처럼 부드럽게 달려요!)",
        
        "c_general_pro": "🎯 <b>[칭찬 및 강점]</b> 기본 자세와 시선 처리가 엘리트 선수급입니다.<br>⚖️ <b>[장단점 분석]</b> 진입 속도는 좋으나, 마지막 에너지 전이가 약합니다.<br>🚨 <b>[문제 진단]</b> <b>{avg_angle}°</b> 측정 (<b>{gap:.1f}° 편차</b>). 키네틱 체인이 단절되어 폭발력 누수.<br>💡 <b>[해결 및 훈련법]</b> 1. 관절 가동성 훈련 2. 힘쓰기 직전 무게중심(COM) 하강 제어 3. 상하체 타이밍 동기화",
        "c_general_kids": "🌟 <b>[Great Job! 최고예요]</b> You look like a champion! (챔피언 같아요!)<br>🔍 <b>[Pros & Cons 장단점]</b> Good focus, but use your whole body! (집중력은 좋은데, 온몸을 써보세요!)<br>🚀 <b>[Superhero Move 히어로 놀이]</b> Shrink like a spring, then explode! (용수철처럼 움츠렸다가 폭발하세요!)",
        
        "vision_title": "🛰️ Future Mission: 글로벌 표준 데이터화", "vision_desc": "글로벌 15개 육상 종목의 데이터를 구글 AR 안경에 투사하는 파운데이션 플랫폼입니다.", "f_title": "🧪 AI 연구소", "f_desc": "여러분의 피드백이 AI를 성장시킵니다."
    },
    "🇺🇸 English": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Global Biomechanics Foundation Digitizing Human Movement",
        "s_head": "⚙️ Settings", "s_cat": "🏟️ Category", "s_sport": "🏃‍♂️ Event", "s_data": "📊 Benchmark", "s_up": "Upload Video", "s_btn": "🚀 Run AI Coaching", "r_title": "🔬 AI Biomechanics Report", "img_title": "📸 Vision AI Skeletal Tracking", "tab_pro": "🎓 Pro Biomechanics", "tab_kids": "🎈 Easy English Kids", "toss": "💙 Support via Toss: ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[Praise]</b> Excellent initial acceleration.<br>⚖️ <b>[Pros & Cons]</b> Good arm drive, weak ground force.<br>🚨 <b>[Diagnosis]</b> Knee ext <b>{avg_angle}°</b>. <b>{gap:.1f}° early recovery</b> causes SSC leak.<br>💡 <b>[Solution]</b> 1. Depth jumps 2. Forefoot strike 3. Arm-leg sync",
        "c_sprint_kids": "🌟 <b>[Great Job!]</b> You run so fast!<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less!<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly with your toes!",
        "c_mara_pro": "🎯 <b>[Praise]</b> Stable upper body.<br>⚖️ <b>[Pros & Cons]</b> Great endurance, poor energy efficiency.<br>🚨 <b>[Diagnosis]</b> <b>{gap:.1f}° deviation</b>. Vertical GRF dispersion.<br>💡 <b>[Solution]</b> 1. Iliopsoas stretch 2. Single-leg deadlift 3. Midfoot strike",
        "c_mara_kids": "🌟 <b>[Great Job!]</b> Amazing energy!<br>🔍 <b>[Pros & Cons]</b> Good breathing, but don't bounce!<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! Glide like a ninja!",
        "c_general_pro": "🎯 <b>[Praise]</b> Elite-level basic posture.<br>⚖️ <b>[Pros & Cons]</b> Good speed, weak final energy transfer.<br>🚨 <b>[Diagnosis]</b> <b>{avg_angle}°</b> (<b>{gap:.1f}° deviation</b>). Weak kinetic chain.<br>💡 <b>[Solution]</b> 1. Mobility drills 2. COM drop control 3. Timing sync",
        "c_general_kids": "🌟 <b>[Great Job!]</b> You look like a champion!<br>🔍 <b>[Pros & Cons]</b> Good focus, but use your whole body!<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode!",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Projecting global athletics data into AR glasses.", "f_title": "🧪 AI Lab", "f_desc": "Leave your feedback."
    },
    "🇯🇵 日本語": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "人類のすべての動きをデータ化するバイオメカニクスAI",
        "s_head": "⚙️ 設定", "s_cat": "🏟️ カテゴリ", "s_sport": "🏃‍♂️ 種目", "s_data": "📊 比較対象", "s_up": "動画アップロード", "s_btn": "🚀 AI分析実行", "r_title": "🔬 AI診断レポート", "img_title": "📸 AI骨格トラッキング", "tab_pro": "🎓 プロフェッショナル分析", "tab_kids": "🎈 子供向け英語体育 (Kids)", "toss": "💙 支援 (Toss): ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[称賛]</b> 素晴らしい初期加速です。<br>⚖️ <b>[長所・短所]</b> 腕の振りは良いが、推進力が不足。<br>🚨 <b>[課題診断]</b> 膝の伸展 <b>{avg_angle}°</b>。<b>{gap:.1f}°の早期回収</b>。<br>💡 <b>[練習法]</b> 1. デプスジャンプ 2. フォアフット接地 3. 連動",
        "c_sprint_kids": "🌟 <b>[Great Job! すごい！]</b> You run so fast! (速いね！)<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less! (腕は良いけど膝を伸ばそう！)<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly! (床がマグマだよ！素早くタッチ！)",
        "c_mara_pro": "🎯 <b>[称賛]</b> 安定した上半身と呼吸。<br>⚖️ <b>[長所・短所]</b> 持久力は高いが効率が低下。<br>🚨 <b>[課題診断]</b> <b>{gap:.1f}°の偏差</b>。GRFが垂直に分散。<br>💡 <b>[練習法]</b> 1. 腸腰筋ストレッチ 2. 体幹安定化 3. ミッドフット接地",
        "c_mara_kids": "🌟 <b>[Great Job! すごい！]</b> Amazing energy! (エネルギーがあふれてるね！)<br>🔍 <b>[Pros & Cons]</b> Good breathing, but don't bounce! (呼吸は良いけど弾まないように！)<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! (頭にコップを乗せて忍者のように走ろう！)",
        "c_general_pro": "🎯 <b>[称賛]</b> 基本姿勢がエリートレベル。<br>⚖️ <b>[長所・短所]</b> 進入速度は良いが力の伝達が弱い。<br>🚨 <b>[課題診断]</b> <b>{avg_angle}°</b>（<b>{gap:.1f}°の偏差</b>）。キネティックチェーンの切断。<br>💡 <b>[練習法]</b> 1. 可動域 2. 重心の沈み込み 3. 連動",
        "c_general_kids": "🌟 <b>[Great Job! すごい！]</b> You look like a champion! (チャンピオンみたい！)<br>🔍 <b>[Pros & Cons]</b> Good focus, but use your whole body! (全身を使ってみよう！)<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode! (バネみたいに縮んで爆発だ！)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "世界の陸上データをARグラスに投影するプラットフォーム。", "f_title": "🧪 AI研究所", "f_desc": "フィードバックをお願いします。"
    },
    "🇨🇳 中文": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "将人类所有运动数据化的全球田径生物力学基础模型",
        "s_head": "⚙️ 系统设置", "s_cat": "🏟️ 类别", "s_sport": "🏃‍♂️ 项目", "s_data": "📊 对比基准", "s_up": "上传视频", "s_btn": "🚀 运行 AI 诊断", "r_title": "🔬 AI 生物力学报告", "img_title": "📸 视觉 AI 骨骼追踪", "tab_pro": "🎓 专家级深入诊断", "tab_kids": "🎈 儿童英语体育 (Kids)", "toss": "💙 赞助 (Toss): ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[表扬]</b> 极佳的初始加速。<br>⚖️ <b>[优缺点分析]</b> 手臂摆动好，但下肢蹬地力不足。<br>🚨 <b>[问题诊断]</b> 膝伸展 <b>{avg_angle}°</b>。<b>{gap:.1f}° 的提前回收</b>。<br>💡 <b>[训练]</b> 1. 深度跳跃 2. 前脚掌着地 3. 手脚同步",
        "c_sprint_kids": "🌟 <b>[Great Job! 太棒了]</b> You run so fast! (跑得真快！)<br>🔍 <b>[Pros & Cons 优缺点]</b> Good arms, but bend knees less! (手臂动作很好，伸直膝盖哦！)<br>🔥 <b>[Hot Lava Game 岩浆游戏]</b> The ground is hot lava! Touch it quickly! (地面是岩浆！用脚尖快速点地！)",
        "c_mara_pro": "🎯 <b>[表扬]</b> 稳定的上半身和呼吸。<br>⚖️ <b>[优缺点分析]</b> 耐力强，但能量利用率低。<br>🚨 <b>[问题诊断]</b> <b>{gap:.1f}° 偏差</b>。反作用力垂直分散。<br>💡 <b>[训练]</b> 1. 髂腰肌拉伸 2. 单腿硬拉 3. 中足着地",
        "c_mara_kids": "🌟 <b>[Great Job! 太棒了]</b> Amazing energy! (活力满满！)<br>🔍 <b>[Pros & Cons 优缺点]</b> Good breathing, but don't bounce! (呼吸很好，但不要上下蹦跳！)<br>💧 <b>[Water Cup Game 水杯游戏]</b> Imagine a water cup on your head! (想象头顶有杯水，像忍者一样滑行！)",
        "c_general_pro": "🎯 <b>[表扬]</b> 精英级别的基本姿势。<br>⚖️ <b>[优缺点分析]</b> 助跑快，但能量转移弱。<br>🚨 <b>[问题诊断]</b> <b>{avg_angle}°</b>（<b>{gap:.1f}° 偏差</b>）。动力链断裂。<br>💡 <b>[训练]</b> 1. 关节活动度 2. 重心下降 3. 同步",
        "c_general_kids": "🌟 <b>[Great Job! 太棒了]</b> You look like a champion! (像个冠军！)<br>🔍 <b>[Pros & Cons 优缺点]</b> Good focus, but use your whole body! (注意力集中，试着用全身发力！)<br>🚀 <b>[Superhero Move 超人动作]</b> Shrink like a spring, then explode! (像弹簧一样收缩，然后爆发！)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "将田径数据投射到AR眼镜的平台。", "f_title": "🧪 AI 实验室", "f_desc": "期待您的反馈。"
    },
    "🇪🇸 Español": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "Biomecánica global que digitaliza el movimiento",
        "s_head": "⚙️ Ajustes", "s_cat": "🏟️ Categoría", "s_sport": "🏃‍♂️ Evento", "s_data": "📊 Referencia", "s_up": "Subir Video", "s_btn": "🚀 Ejecutar AI", "r_title": "🔬 Reporte Biomecánico AI", "img_title": "📸 Seguimiento de Esqueleto", "tab_pro": "🎓 Diagnóstico Pro", "tab_kids": "🎈 Inglés y Juego (Kids)", "toss": "💙 Apoyo (Toss): ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[Elogio]</b> Excelente aceleración inicial.<br>⚖️ <b>[Pros y Contras]</b> Buen braceo, falta fuerza de despegue.<br>🚨 <b>[Diagnóstico]</b> Extensión <b>{avg_angle}°</b>. <b>{gap:.1f}° recuperación temprana</b>.<br>💡 <b>[Solución]</b> 1. Saltos de profundidad 2. Punta del pie 3. Sincronización",
        "c_sprint_kids": "🌟 <b>[Great Job! ¡Genial!]</b> You run so fast! (¡Corres muy rápido!)<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less! (¡Buenos brazos, estira las rodillas!)<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly! (¡El suelo es lava! ¡Tócalo rápido!)",
        "c_mara_pro": "🎯 <b>[Elogio]</b> Ritmo estable.<br>⚖️ <b>[Pros y Contras]</b> Gran resistencia, baja eficiencia.<br>🚨 <b>[Diagnóstico]</b> <b>{gap:.1f}° desviación</b>. Dispersión de energía.<br>💡 <b>[Solución]</b> 1. Estiramiento de psoas 2. Peso muerto 3. Aterrizaje medio",
        "c_mara_kids": "🌟 <b>[Great Job! ¡Genial!]</b> Amazing energy! (¡Energía increíble!)<br>🔍 <b>[Pros & Cons]</b> Good breathing, but don't bounce! (¡Buena respiración, no rebotes!)<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! (¡Imagina un vaso de agua en tu cabeza!)",
        "c_general_pro": "🎯 <b>[Elogio]</b> Postura de élite.<br>⚖️ <b>[Pros y Contras]</b> Buena velocidad, débil transferencia.<br>🚨 <b>[Diagnóstico]</b> <b>{avg_angle}°</b> (<b>{gap:.1f}° desviación</b>). Cadena cinética rota.<br>💡 <b>[Solución]</b> 1. Movilidad 2. Control COM 3. Sincronización",
        "c_general_kids": "🌟 <b>[Great Job! ¡Genial!]</b> You look like a champion! (¡Pareces campeón!)<br>🔍 <b>[Pros & Cons]</b> Good focus, but use your whole body! (¡Usa todo tu cuerpo!)<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode! (¡Encógete como un resorte y explota!)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Proyectando datos a gafas AR.", "f_title": "🧪 Laboratorio AI", "f_desc": "Deja tus comentarios."
    },
    "🇮🇳 हिन्दी (Hindi)": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "ग्लोबल बायोमैकेनिक्स सिस्टम",
        "s_head": "⚙️ सेटिंग्स", "s_cat": "🏟️ श्रेणी", "s_sport": "🏃‍♂️ खेल", "s_data": "📊 बेंचमार्क", "s_up": "वीडियो अपलोड करें", "s_btn": "🚀 AI विश्लेषण", "r_title": "🔬 AI बायोमैकेनिक्स रिपोर्ट", "img_title": "📸 AI कंकाल ट्रैकिंग", "tab_pro": "🎓 पेशेवर विश्लेषण", "tab_kids": "🎈 बच्चों के लिए खेल (Kids)", "toss": "💙 Toss द्वारा समर्थन: ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[प्रशंसा]</b> बहुत बढ़िया प्रारंभिक त्वरण।<br>⚖️ <b>[पेशेवर और विपक्ष]</b> अच्छे हाथ, कमजोर पैर।<br>🚨 <b>[निदान]</b> घुटने का विस्तार <b>{avg_angle}°</b>। <b>{gap:.1f}° विचलन</b>।<br>💡 <b>[समाधान]</b> 1. डेप्थ जंप 2. फोरफुट 3. सिंक",
        "c_sprint_kids": "🌟 <b>[Great Job! बहुत बढ़िया!]</b> You run so fast! (तुम बहुत तेज दौड़ते हो!)<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less! (घुटने सीधे करो!)<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly! (जमीन लावा है! जल्दी छुओ!)",
        "c_mara_pro": "🎯 <b>[प्रशंसा]</b> स्थिर शरीर।<br>⚖️ <b>[पेशेवर और विपक्ष]</b> अच्छी सहनशक्ति, खराब दक्षता।<br>🚨 <b>[निदान]</b> <b>{gap:.1f}° विचलन</b>। ऊर्जा लंबवत फैलती है।<br>💡 <b>[समाधान]</b> 1. स्ट्रेचिंग 2. डेडलिफ्ट 3. मिडफुट",
        "c_mara_kids": "🌟 <b>[Great Job! बहुत बढ़िया!]</b> Amazing energy! (अद्भुत ऊर्जा!)<br>🔍 <b>[Pros & Cons]</b> Good breathing, but don't bounce! (उछलो मत!)<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! (सिर पर पानी का गिलास सोचो!)",
        "c_general_pro": "🎯 <b>[प्रशंसा]</b> एलीट लेवल मुद्रा।<br>⚖️ <b>[पेशेवर और विपक्ष]</b> अच्छी गति, कमजोर ऊर्जा।<br>🚨 <b>[निदान]</b> <b>{avg_angle}°</b> (<b>{gap:.1f}° विचलन</b>)।<br>💡 <b>[समाधान]</b> 1. गतिशीलता 2. COM ड्रॉप 3. समय",
        "c_general_kids": "🌟 <b>[Great Job! बहुत बढ़िया!]</b> You look like a champion! (तुम चैंपियन लगते हो!)<br>🔍 <b>[Pros & Cons]</b> Good focus, but use your whole body! (पूरे शरीर का उपयोग करो!)<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode! (स्प्रिंग की तरह सिकुड़ें!)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "एआर चश्मे में वैश्विक डेटा पेश करना।", "f_title": "🧪 AI लैब", "f_desc": "अपनी प्रतिक्रिया दें।"
    },
    "🇫🇷 Français": {
        "title": "ATHLETICS AI FOUNDATION", "sub": "La Fondation Biomécanique Mondiale",
        "s_head": "⚙️ Paramètres", "s_cat": "🏟️ Catégorie", "s_sport": "🏃‍♂️ Événement", "s_data": "📊 Référence (Pays)", "s_up": "Télécharger Vidéo", "s_btn": "🚀 Lancer le Coaching AI", "r_title": "🔬 Rapport Biomécanique AI", "img_title": "📸 Suivi Squelettique AI", "tab_pro": "🎓 Diagnostic Pro", "tab_kids": "🎈 Kids (Anglais Facile)", "toss": "💙 Soutenir (Toss): ATHLETICS AI",
        "c_sprint_pro": "🎯 <b>[Éloges]</b> Excellente accélération initiale.<br>⚖️ <b>[Avantages et Inconvénients]</b> Bon mouvement des bras, faible force d'appui.<br>🚨 <b>[Diagnostic]</b> Extension <b>{avg_angle}°</b>. <b>{gap:.1f}° récupération précoce</b>.<br>💡 <b>[Solution]</b> 1. Sauts profonds 2. Frappe avant-pied 3. Synchronisation",
        "c_sprint_kids": "🌟 <b>[Great Job! Super !]</b> You run so fast! (Tu cours si vite !)<br>🔍 <b>[Pros & Cons]</b> Good arms, but bend knees less! (Bons bras, étire les genoux !)<br>🔥 <b>[Hot Lava Game]</b> The ground is hot lava! Touch it quickly! (Le sol est de la lave ! Touche-le vite !)",
        "c_mara_pro": "🎯 <b>[Éloges]</b> Tronc et respiration stables.<br>⚖️ <b>[Avantages et Inconvénients]</b> Grande endurance, faible efficacité.<br>🚨 <b>[Diagnostic]</b> <b>{gap:.1f}° déviation</b>. Dispersion verticale de l'énergie.<br>💡 <b>[Solution]</b> 1. Étirement du psoas 2. Soulevé de terre 3. Frappe médio-pied",
        "c_mara_kids": "🌟 <b>[Great Job! Super !]</b> Amazing energy! (Une énergie incroyable !)<br>🔍 <b>[Pros & Cons]</b> Good breathing, but don't bounce! (Bonne respiration, mais ne rebondis pas !)<br>💧 <b>[Water Cup Game]</b> Imagine a water cup on your head! (Imagine un verre d'eau sur ta tête !)",
        "c_general_pro": "🎯 <b>[Éloges]</b> Posture de niveau élite.<br>⚖️ <b>[Avantages et Inconvénients]</b> Bonne vitesse, transfert d'énergie faible.<br>🚨 <b>[Diagnostic]</b> <b>{avg_angle}°</b> (<b>{gap:.1f}° déviation</b>). Chaîne cinétique brisée.<br>💡 <b>[Solution]</b> 1. Mobilité 2. Contrôle du centre de masse 3. Synchronisation",
        "c_general_kids": "🌟 <b>[Great Job! Super !]</b> You look like a champion! (Tu ressembles à un champion !)<br>🔍 <b>[Pros & Cons]</b> Good focus, but use your whole body! (Utilise tout ton corps !)<br>🚀 <b>[Superhero Move]</b> Shrink like a spring, then explode! (Comprime-toi comme un ressort et explose !)",
        "vision_title": "🛰️ Future Mission", "vision_desc": "Projection de données mondiales dans des lunettes AR.", "f_title": "🧪 Laboratoire AI", "f_desc": "Laissez vos commentaires."
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

# 🚀 벤치마크 DB 대폭 확장 (미국, 일본, 중국, 인도, 프랑스 등)
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
    _import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; color: #202124; }
    .hero-section { background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #233554 100%); padding: 50px 20px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
    .hero-title { color: #64FFDA; font-size: 3.5em; font-weight: 900; letter-spacing: 2px; margin: 0 0 10px 0; text-shadow: 0px 4px 15px rgba(100, 255, 218, 0.3); }
    .hero-sub { color: #CCD6F6; font-size: 1.2em; font-weight: 400; margin: 0; }
    .data-card { background: white; padding: 25px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #E8EAED; height: 100%; }
    .coaching-box { background: #FFFFFF; border-top: 5px solid #1A73E8; padding: 30px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); height: 100%; line-height: 1.6; }
    .toss-btn { display: inline-block; background: #3182F6; color: white !important; font-weight: 800; padding: 12px 24px; border-radius: 30px; text-decoration: none; margin-top: 15px; box-shadow: 0 4px 15px rgba(49, 130, 246, 0.4); }
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

# 🚀 첫 화면 전면 배치 (Hero Section & Toss ID 복구)
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">{t['title']}</h1>
        <p class="hero-sub">{t['sub']}</p>
        <a href="#" class="toss-btn">{t['toss']}</a>
    </div>
    """, unsafe_allow_html=True)

# 6. 메인 딥러닝 분석 시뮬레이션
if video_file and analyze_btn:
    with st.spinner('AI Analytics & Multi-language Processing...'):
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
        tab_pro, tab_kids = st.tabs([t['tab_pro'], t['tab_kids']])
        
        # 종목별 코칭 (7대 언어 동적 매핑)
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
st.markdown(f"""
    <div style="background: linear-gradient(to right, #E8F0FE, #FFFFFF); border-left: 5px solid #1A73E8; padding: 30px; border-radius: 12px;">
        <h3 style="color: #1A73E8; margin-top: 0;">{t['vision_title']}</h3><p style="font-size: 1.1em; color: #3C4043;">{t['vision_desc']}</p>
    </div>
""", unsafe_allow_html=True)

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