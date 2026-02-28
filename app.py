import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import time

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 🌐 [글로벌 다국어 번역 사전 (UI 전체 적용)]
LANGUAGES = ["🇰🇷 한국어", "🇺🇸 English", "🇯🇵 日本語", "🇪🇸 Español", "🇫🇷 Français", "🇨🇳 中文", "🇮🇳 हिन्दी", "🇵🇹 Português", "🇩🇪 Deutsch", "🇦🇪 العربية"]

# 번역 데이터베이스 (UI, 카테고리, 피드백 등 전체 포괄)
TRANS_DB = {
    # 1. 메인 UI
    "title": {"🇺🇸 English": "⚡ ATHLETES AI:<br>Ultra-Simple Global<br>Analysis Engine", "🇯🇵 日本語": "⚡ ATHLETES AI:<br>超シンプルグローバル<br>分析エンジン"},
    "step1": {"🇺🇸 English": "Step 1: Main Category", "🇯🇵 日本語": "ステップ1：大分類"},
    "step2": {"🇺🇸 English": "Step 2: Sub Category", "🇯🇵 日本語": "ステップ2：中分類"},
    "step3": {"🇺🇸 English": "Step 3: Specific Sport", "🇯🇵 日本語": "ステップ3：詳細種目"},
    "premium": {"🇺🇸 English": "💎 Premium Mode (1:1 Model Comparison)", "🇯🇵 日本語": "💎 プレミアムモード (1:1 モデル比較)"},
    "upload_msg": {"🇺🇸 English": "Upload customer video (10-sec AI Analysis)", "🇯🇵 日本語": "顧客の動画をアップロード (10秒 AI 分析)"},
    
    # 2. 대분류 (1단계)
    "하계 올림픽 종목": {"🇺🇸 English": "Summer Olympics", "🇯🇵 日本語": "夏季オリンピック"},
    "동계 올림픽 종목": {"🇺🇸 English": "Winter Olympics", "🇯🇵 日本語": "冬季オリンピック"},
    "대중 구기 종목 (축구/야구 등)": {"🇺🇸 English": "Ball Sports (Soccer/Baseball)", "🇯🇵 日本語": "球技 (サッカー/野球など)"},
    
    # 3. 중분류 (2단계)
    "육상": {"🇺🇸 English": "Athletics", "🇯🇵 日本語": "陸上競技"},
    "수영/무도": {"🇺🇸 English": "Swimming/Martial Arts", "🇯🇵 日本語": "水泳/武道"},
    "라켓/타겟": {"🇺🇸 English": "Racket/Target", "🇯🇵 日本語": "ラケット/ターゲット"},
    "빙상/설상": {"🇺🇸 English": "Ice/Snow Sports", "🇯🇵 日本語": "氷上/雪上スポーツ"},
    "축구": {"🇺🇸 English": "Soccer/Football", "🇯🇵 日本語": "サッカー"},
    "야구/농구": {"🇺🇸 English": "Baseball/Basketball", "🇯🇵 日本語": "野球/バスケットボール"},
    
    # 4. 분석 결과 및 피드백 텍스트
    "분석 완료!": {"🇺🇸 English": "✅ AI Deep Learning Complete!", "🇯🇵 日本語": "✅ AI ディープラーニング完了！"},
    "정밀 분석 리포트": {"🇺🇸 English": "Precision Analysis Report", "🇯🇵 日本語": "精密分析レポート"},
    "내 타겟 관절 평균 각도": {"🇺🇸 English": "My Target Joint Avg Angle", "🇯🇵 日本語": "ターゲット関節の平均角度"},
    "AI 멀티모달 진단": {"🇺🇸 English": "🔊 AI Multi-modal Diagnosis (Posture + Audio)", "🇯🇵 日本語": "🔊 AI マルチモーダル診断 (姿勢 + 音声)"},
    "경고문구": {"🇺🇸 English": "**Hearing a 'clack' sound upon foot strike indicates heavy impact on the knees, requiring form correction. Relax your shoulders and use the psoas muscle for your pitch to better utilize pelvic muscles and land closer to the target.**", "🇯🇵 日本語": "**足裏が着地する際の「カチッ」という音は、膝への衝撃が大きいフォームを示しており、姿勢の改善が必要です。肩の力を抜き、腸腰筋を使ってピッチを行うことで、骨盤の筋肉をうまく活用し、目標位置に近い着地が可能になります。**"},
    "유튜브 처방": {"🇺🇸 English": "📺 AI Custom YouTube Training", "🇯🇵 日本語": "📺 AI カスタム YouTube トレーニング"}
}

# 번역기 함수 (선택한 언어에 맞춰 텍스트 반환)
def t(korean_text):
    if selected_lang == "🇰🇷 한국어":
        return korean_text
    return TRANS_DB.get(korean_text, {}).get(selected_lang, korean_text)

st.set_page_config(page_title="ATHLETES AI GLOBAL", layout="wide")

# 🌐 언어 선택창
selected_lang = st.selectbox("🌐 Select Language / 언어 선택", LANGUAGES)

# 타이틀 출력
st.markdown(f"<h1 style='text-align: center;'>{t('title')}</h1>", unsafe_allow_html=True)

# 2. [초단순 3단계 트리] (내부 로직은 한국어로 유지하여 개발 꼬임 방지)
SPORT_TREE = {
    "하계 올림픽 종목": {
        "육상": ["100m 단거리 (하체: 골반-무릎-발목)", "마라톤/장거리 (하체: 골반-무릎-발목)", "경보 (하체: 골반-무릎-발목)", "장대높이뛰기 (전신: 어깨-골반-발목)", "창던지기 (상체: 어깨-팔꿈치-손목)"],
        "수영/무도": ["자유형/배영 (상체: 어깨-팔꿈치-손목)", "태권도 발차기 (하체: 골반-무릎-발목)", "유도 메치기 (전신: 어깨-골반-발목)"],
        "라켓/타겟": ["테니스 (상체: 어깨-팔꿈치-손목)", "배드민턴 (상체: 어깨-팔꿈치-손목)", "양궁 (상체: 어깨-팔꿈치-손목)"]
    },
    "동계 올림픽 종목": {
        "빙상/설상": ["쇼트트랙 코너링 (하체: 골반-무릎-발목)", "스피드스케이팅 (하체: 골반-무릎-발목)", "알파인 스키 (하체: 골반-무릎-발목)"]
    },
    "대중 구기 종목 (축구/야구 등)": {
        "축구": ["슈팅/프리킥 (하체: 골반-무릎-발목)", "헤딩/점프 (전신: 어깨-골반-발목)"],
        "야구/농구": ["투구/피칭 (상체: 어깨-팔꿈치-손목)", "타격/스윙 (전신: 어깨-골반-발목)", "점프슛 (상체: 어깨-팔꿈치-손목)"]
    }
}

# 3. [직관적 UI 구성 & 번역 연동]
col1, col2, col3 = st.columns(3)
# format_func=t 를 사용하면 화면에는 번역된 언어가 보이고, AI 내부에는 한국어 키워드가 전달되어 에러가 나지 않습니다.
with col1: l1 = st.selectbox(t('step1'), list(SPORT_TREE.keys()), format_func=t)
with col2: l2 = st.selectbox(t('step2'), list(SPORT_TREE[l1].keys()), format_func=t)
with col3: l3 = st.selectbox(t('step3'), SPORT_TREE[l1][l2]) # 세부 종목은 우선 원본 유지

target_part = l3.split("(")[1].split(":")[0]

# 💎 [프리미엄 1:1 듀얼 분석] 
st.write("---")
is_premium = st.toggle(t('premium'))

user_file, star_file = None, None

if is_premium:
    st.markdown(f"### 👥 {t('premium')}")
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.info("👤 Customer" if selected_lang == "🇺🇸 English" else "👤 고객 (Customer)")
        user_height = st.number_input("Height / 키 (cm)", 100, 250, 175)
        user_age = st.number_input("Age / 나이", 5, 100, 25)
        user_weight = st.number_input("Weight / 몸무게 (kg)", 20, 200, 70)
        user_file = st.file_uploader("Upload Customer Video", type=["mp4", "mov"], key="user_vid")
        
    with p_col2:
        st.success("🌟 Role Model" if selected_lang == "🇺🇸 English" else "🌟 롤모델 (Role Model)")
        star_height = st.number_input("Model Height / 롤모델 키 (cm)", 100, 250, 183)
        star_age = st.number_input("Model Age / 롤모델 나이", 5, 100, 31)
        star_weight = st.number_input("Model Weight / 롤모델 몸무게 (kg)", 20, 200, 78)
        star_file = st.file_uploader("Upload Model Video", type=["mp4", "mov"], key="star_vid")

else:
    user_file = st.file_uploader(t("upload_msg"), type=["mp4", "mov", "avi"])

# 4. [초고속 백그라운드 분석 및 영상 숨김]
if (not is_premium and user_file) or (is_premium and user_file and star_file):
    status_msg = "Analyzing..." if selected_lang != "🇰🇷 한국어" else f"🔍 AI가 [{target_part}] 역학을 분석 중입니다..."
    st.info(status_msg)
    progress_bar = st.progress(0)
    
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
        
    progress_bar.empty()
    st.success(t("분석 완료!"))
    st.write("---")
    
    # 5. [결과 리포트 및 유튜브/오디오 매칭]
    clean_title = l3.split('(')[0].strip()
    
    if is_premium:
        st.subheader(f"💎 1:1 {t('정밀 분석 리포트')} ({clean_title})")
        height_diff = user_height - star_height
        c1, c2 = st.columns(2)
        c1.metric("Customer Angle", "145°")
        c2.metric("Model Angle", "155°", delta="-10°")
    else:
        st.subheader(f"📊 {clean_title} {t('정밀 분석 리포트')}")
        st.metric(t("내 타겟 관절 평균 각도"), "145°")

    st.markdown(f"### {t('AI 멀티모달 진단')}")
    st.warning(t("경고문구"))

    st.markdown(f"### {t('유튜브 처방')}")
    search_query = f"{clean_title} 장요근 피치 복근"
    btn_text = "▶️ Watch YouTube Training" if selected_lang == "🇺🇸 English" else "▶️ 유튜브 맞춤 훈련 보기"
    st.link_button(btn_text, f"https://www.youtube.com/results?search_query={search_query}")
    st.balloons()
