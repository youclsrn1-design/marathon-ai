import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import time
import math

# 1. AI 엔진 설정 (Real MediaPipe)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 🌐 한/영 완벽 번역 사전 
LANGUAGES = ["🇰🇷 한국어", "🇺🇸 English"]

TRANS_DICT = {
    "⚡ ATHLETES AI:<br>초단순 글로벌<br>분석 엔진": "⚡ ATHLETES AI:<br>Ultra-Simple Global<br>Analysis Engine",
    "1단계: 대분류": "Step 1: Main Category", "2단계: 중분류": "Step 2: Sub Category", "3단계: 세부 종목 및 분석 타겟": "Step 3: Specific Sport & Target",
    "💎 프리미엄 모드 (롤모델 1:1 비교)": "💎 Premium Mode (1:1 Model Comparison)",
    "고객 영상을 업로드하세요. (AI 실시간 백그라운드 분석)": "Upload Customer Video (AI Real-time Analysis)",
    "하계 올림픽 종목": "Summer Olympics", "동계 올림픽 종목": "Winter Olympics", "대중 구기 종목 (축구/야구 등)": "Popular Ball Sports",
    "육상": "Athletics", "수영/무도": "Swimming / Martial Arts", "라켓/타겟": "Racket / Target",
    "빙상/설상": "Ice / Snow Sports", "축구": "Soccer", "야구/농구": "Baseball / Basketball",
    "100m 단거리 (하체: 골반-무릎-발목)": "100m Sprint (Lower Body)", "마라톤/장거리 (하체: 골반-무릎-발목)": "Marathon (Lower Body)", "경보 (하체: 골반-무릎-발목)": "Racewalking (Lower Body)", "장대높이뛰기 (전신: 어깨-골반-발목)": "Pole Vault (Full Body)", "창던지기 (상체: 어깨-팔꿈치-손목)": "Javelin Throw (Upper Body)", "자유형/배영 (상체: 어깨-팔꿈치-손목)": "Freestyle/Backstroke (Upper)", "태권도 발차기 (하체: 골반-무릎-발목)": "Taekwondo Kick (Lower)", "유도 메치기 (전신: 어깨-골반-발목)": "Judo Throw (Full Body)", "테니스 (상체: 어깨-팔꿈치-손목)": "Tennis (Upper Body)", "배드민턴 (상체: 어깨-팔꿈치-손목)": "Badminton (Upper Body)", "양궁 (상체: 어깨-팔꿈치-손목)": "Archery (Upper Body)", "쇼트트랙 코너링 (하체: 골반-무릎-발목)": "Short Track Cornering (Lower)", "스피드스케이팅 (하체: 골반-무릎-발목)": "Speed Skating (Lower Body)", "알파인 스키 (하체: 골반-무릎-발목)": "Alpine Skiing (Lower Body)", "슈팅/프리킥 (하체: 골반-무릎-발목)": "Shooting/Free Kick (Lower)", "헤딩/점프 (전신: 어깨-골반-발목)": "Header/Jump (Full Body)", "투구/피칭 (상체: 어깨-팔꿈치-손목)": "Pitching (Upper Body)", "타격/스윙 (전신: 어깨-골반-발목)": "Batting/Swing (Full Body)", "점프슛 (상체: 어깨-팔꿈치-손목)": "Jump Shoot (Upper Body)",
    "### 👥 1:1 맞춤형 롤모델 정밀 비교 시스템": "### 👥 1:1 Role Model Precision Comparison",
    "👤 고객 (Customer) 정보 및 영상": "👤 Customer Info & Video", "고객 키 (cm)": "Customer Height (cm)", "고객 나이 (세)": "Customer Age", "고객 몸무게 (kg)": "Customer Weight (kg)", "고객 영상 업로드": "Upload Customer Video",
    "🌟 롤모델 (Role Model) 정보 및 영상": "🌟 Role Model Info & Video", "롤모델 키 (cm)": "Model Height (cm)", "롤모델 나이 (세)": "Model Age", "롤모델 몸무게 (kg)": "Model Weight (kg)", "롤모델 영상 업로드": "Upload Model Video",
    "정밀 분석 리포트": "Precision Analysis Report", "프리미엄 1:1 분석 리포트": "Premium 1:1 Analysis Report",
    "고객 타겟 평균 각도": "Customer Target Angle", "롤모델 타겟 평균 각도": "Role Model Target Angle", "내 타겟 관절 평균 각도": "My Target Joint Angle",
    "### ⚖️ 신체 스펙 보정 정밀 진단": "### ⚖️ Body Spec Precision Diagnosis",
    "### 🔍 AI 동적 자세 진단 (Dynamic Posture Analysis)": "### 🔍 AI Dynamic Posture Analysis",
    "### 📺 구글 AI 맞춤 유튜브 훈련 처방": "### 📺 Google AI Custom YouTube Training",
    "▶️ 전 세계 유튜브 맞춤형 영상 보기": "▶️ Watch Custom YouTube Training Video"
}

def t(kr_text):
    if selected_lang == "🇰🇷 한국어": return kr_text
    return TRANS_DICT.get(kr_text, kr_text)

# 💡 [진짜 AI 코어] 업로드된 영상에서 뼈대를 추출하고 실제 삼각함수 각도를 계산합니다.
def analyze_real_video(video_file, target_part):
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    angles = []
    frame_count = 0
    # 속도를 위해 3프레임당 1번씩 실제 분석 (Real-time 최적화)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_count += 1
        if frame_count % 3 != 0: continue 

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            # 부위별 실제 좌표 추출
            if target_part == "상체":
                a, b, c = [lm[11].x, lm[11].y], [lm[13].x, lm[13].y], [lm[15].x, lm[15].y] # 어깨-팔꿈치-손목
            elif target_part == "전신":
                a, b, c = [lm[11].x, lm[11].y], [lm[23].x, lm[23].y], [lm[27].x, lm[27].y] # 어깨-골반-발목
            else: # 하체
                a, b, c = [lm[23].x, lm[23].y], [lm[25].x, lm[25].y], [lm[27].x, lm[27].y] # 골반-무릎-발목
            
            # 삼각함수로 실제 각도 계산
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            if angle > 180.0: angle = 360 - angle
            angles.append(int(angle))
            
    cap.release()
    # 뼈대가 아예 안 잡힌 영상은 기본값 반환, 잡혔으면 진짜 평균 각도 반환
    return int(np.mean(angles)) if angles else 0

# 💡 실제 각도를 바탕으로 진짜 진단을 내리는 로직
def get_dynamic_feedback(part, angle, lang):
    if angle == 0:
        return "⚠️ 영상에서 사람의 뼈대를 명확히 찾을 수 없습니다. 전신이 잘 보이는 영상을 올려주세요." if lang == "🇰🇷 한국어" else "⚠️ Could not detect posture clearly. Please upload a clear full-body video."
    
    if part == "상체":
        if angle < 140:
            ko = "⚠️ 팔꿈치나 어깨가 너무 굽혀져 힘이 온전히 전달되지 않습니다. 관절을 조금 더 뻗어 궤적을 넓혀보세요."
            en = "⚠️ Your elbows/shoulders are too bent, reducing power transfer. Extend your joints slightly."
        elif angle > 165:
            ko = "⚠️ 관절이 뻣뻣하게 너무 펴져 있어 부상 위험이 높습니다. 팔꿈치에 살짝 여유를 두세요."
            en = "⚠️ Your joints are overextended, increasing injury risk. Keep a slight bend."
        else:
            ko = "✅ 훌륭합니다! 상체 각도가 프로 선수들의 최적 범위 안에 있으며 완벽한 밸런스입니다."
            en = "✅ Excellent! Your upper body angle is within the optimal pro range."
    elif part == "하체":
        if angle < 145:
            ko = "⚠️ 무릎이 너무 굽혀져 체력 소모가 큽니다. 골반을 앞으로 밀어주며 하체 중심을 높이세요."
            en = "⚠️ Your knees are too bent, wasting energy. Push your pelvis forward."
        elif angle > 175:
            ko = "⚠️ 무릎이 충격을 흡수하지 못할 정도로 너무 펴져 있습니다(Knee Lock). 미세하게 굽혀 충격을 분산하세요."
            en = "⚠️ Your knees are too straight (Knee Lock). Bend them slightly to disperse shock."
        else:
            ko = "✅ 완벽합니다! 지면 반발력을 극대화할 수 있는 이상적인 하체 각도를 유지 중입니다."
            en = "✅ Perfect! You are maintaining an ideal lower body angle for maximum force."
    else:
        if angle < 155:
            ko = "⚠️ 코어가 살짝 굽어 하체의 힘이 상체로 전달되지 않습니다. 복근에 힘을 주고 일직선 정렬을 맞추세요."
            en = "⚠️ Your core is bent, stopping power transfer. Tighten your abs and align your body."
        else:
            ko = "✅ 좋습니다! 발끝부터 어깨까지 힘 손실이 없는 완벽한 코어 정렬 상태입니다."
            en = "✅ Good! Your full-body core alignment is perfect, transferring power efficiently."
            
    return en if lang == "🇺🇸 English" else ko

st.set_page_config(page_title="ATHLETES AI GLOBAL", layout="wide")

selected_lang = st.selectbox("🌐 Language / 언어", LANGUAGES)
st.markdown(f"<h1 style='text-align: center;'>{t('⚡ ATHLETES AI:<br>초단순 글로벌<br>분석 엔진')}</h1>", unsafe_allow_html=True)

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

col1, col2, col3 = st.columns(3)
with col1: l1 = st.selectbox(t("1단계: 대분류"), list(SPORT_TREE.keys()), format_func=t)
with col2: l2 = st.selectbox(t("2단계: 중분류"), list(SPORT_TREE[l1].keys()), format_func=t)
with col3: l3 = st.selectbox(t("3단계: 세부 종목 및 분석 타겟"), SPORT_TREE[l1][l2], format_func=t)

target_part = l3.split("(")[1].split(":")[0]

st.write("---")
is_premium = st.toggle(t("💎 프리미엄 모드 (롤모델 1:1 비교)"))

user_file, star_file = None, None

if is_premium:
    st.markdown(t("### 👥 1:1 맞춤형 롤모델 정밀 비교 시스템"))
    p1, p2 = st.columns(2)
    with p1:
        st.info(t("👤 고객 (Customer) 정보 및 영상"))
        u_h = st.number_input(t("고객 키 (cm)"), 100, 250, 175)
        u_w = st.number_input(t("고객 몸무게 (kg)"), 20, 200, 70)
        user_file = st.file_uploader(t("고객 영상 업로드"), type=["mp4", "mov"])
    with p2:
        st.success(t("🌟 롤모델 (Role Model) 정보 및 영상"))
        s_h = st.number_input(t("롤모델 키 (cm)"), 100, 250, 183)
        s_w = st.number_input(t("롤모델 몸무게 (kg)"), 20, 200, 78)
        star_file = st.file_uploader(t("롤모델 영상 업로드"), type=["mp4", "mov"])
else:
    user_file = st.file_uploader(t("고객 영상을 업로드하세요. (AI 실시간 백그라운드 분석)"), type=["mp4", "mov", "avi"])

# 💡 [실제 분석 실행 파트]
if (not is_premium and user_file) or (is_premium and user_file and star_file):
    status_msg = f"🔍 AI extracting and computing REAL [{target_part}] dynamics..." if selected_lang == "🇺🇸 English" else f"🔍 AI가 영상에서 진짜 [{target_part}] 각도 데이터를 추출 중입니다..."
    with st.spinner(status_msg):
        # 1. 고객 영상 진짜 분석
        user_avg = analyze_real_video(user_file, target_part)
        
        # 2. 프리미엄일 경우 롤모델 영상도 진짜 분석
        star_avg = 0
        if is_premium and star_file:
            star_avg = analyze_real_video(star_file, target_part)
            
    st.success(t("✅ AI 딥러닝 분석 완료!"))
    
    clean_title = t(l3)
    
    if is_premium:
        st.subheader(f"💎 {t('프리미엄 1:1 분석 리포트')} ({clean_title})")
        h_diff = u_h - s_h
        c1, c2 = st.columns(2)
        c1.metric(t("고객 타겟 평균 각도"), f"{user_avg}°")
        c2.metric(t("롤모델 타겟 평균 각도"), f"{star_avg}°", delta=f"{user_avg - star_avg}°")
        
        st.markdown(t("### ⚖️ 신체 스펙 보정 정밀 진단"))
        if selected_lang == "🇺🇸 English":
            st.info(f"💡 You are **{abs(h_diff)}cm {'shorter' if h_diff < 0 else 'taller'}** than the model. Adjust your stride {'wider' if h_diff < 0 else 'narrower'} to balance your center of gravity.")
        else:
            st.info(f"💡 고객님은 롤모델보다 키가 **{abs(h_diff)}cm {'작습니다' if h_diff < 0 else '큽니다'}**. 무게중심을 고려해 롤모델보다 보폭을 약간 **{'넓게' if h_diff < 0 else '좁게'} 조정**하는 것이 유리합니다.")
    else:
        st.subheader(f"📊 {clean_title} {t('정밀 분석 리포트')}")
        st.metric(t("내 타겟 관절 평균 각도"), f"{user_avg}°")

    st.markdown(t("### 🔍 AI 동적 자세 진단 (Dynamic Posture Analysis)"))
    dynamic_msg = get_dynamic_feedback(target_part, user_avg, selected_lang)
    if "✅" in dynamic_msg: st.success(dynamic_msg)
    else: st.warning(dynamic_msg)
    
    st.markdown(t("### 📺 구글 AI 맞춤 유튜브 훈련 처방"))
    search_keyword = l3.split('(')[0].strip()
    part_keyword = "코어" if target_part == "전신" else target_part
    
    if selected_lang == "🇺🇸 English":
        st.write(f"💡 **AI Recommendation:** Based on your REAL angle ({user_avg}°), focus on {part_keyword} mobility.")
        search_query = f"{search_keyword} {part_keyword} training drills"
    else:
        st.write(f"💡 **AI 실제 데이터 분석 결과:** 측정된 각도({user_avg}°)를 개선하기 위해 **{search_keyword} {part_keyword} 강화 훈련**이 필요합니다.")
        search_query = f"{search_keyword} {part_keyword} 교정 훈련법"
        
    st.link_button(t("▶️ 전 세계 유튜브 맞춤형 영상 보기"), f"https://www.youtube.com/results?search_query={search_query}")
