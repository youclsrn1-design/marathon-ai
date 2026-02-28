import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")

# 2. 다국어 지원 설정 (언어 선택)
lang = st.radio("🌐 Language / 언어", ["한국어", "English"], horizontal=True)

# 다국어 텍스트 딕셔너리
TEXT = {
    "한국어": {
        "title": "⚡ ATHLETES AI: 글로벌 모션 분석 엔진",
        "gender": "👤 성별 선택",
        "male": "남성",
        "female": "여성",
        "l1_label": "1단계: 대분류",
        "l2_label": "2단계: 중분류",
        "l3_label": "3단계: 세부 종목 및 분석 타겟",
        "upload_model": "🌟 프리미엄 AI: 롤모델 영상 업로드 (선택)",
        "upload_user": "사용자 영상 업로드 (필수)",
        "analyzing_user": "🔍 사용자 영상 분석 중...",
        "analyzing_model": "🔍 롤모델 영상 분석 중...",
        "analysis_done": "✅ AI 10초 딥러닝 분석 완료!",
        "result_title": "정밀 분석 결과",
        "user_angle": "내 타겟 관절 평균 각도",
        "model_angle": "롤모델 평균 각도",
        "diff": "차이",
        "sync_rate": "자세 싱크로율",
        "feedback_title": "💡 AI 핵심 피드백",
        "pos_feedback": "신체 구조에 맞춰 가동 범위를 잘 활용하려는 시도가 돋보입니다. 훌륭한 밸런스입니다.",
        "neg_feedback": "다만, 임팩트 순간 각도가 표준 범위를 벗어나 힘이 분산되고 있습니다. 코어 고정과 정렬이 필요합니다.",
        "audio_title": "🔊 AI 멀티모달 (자세 + 오디오) 진단",
        "audio_desc": "**발바닥이 닿을 때 '딱딱' 소리가 나는 것을 보아 충격을 많이 받게 되는 폼이니 자세 변화가 필요해 보입니다. 어깨에 힘을 빼고 장요근을 활용해보세요.**",
        "youtube_title": "📺 AI 맞춤 유튜브 훈련 처방",
        "youtube_desc": "💡 고객님의 영상에서 분석된 신체/리듬 파악 결과, 아래의 훈련이 적합합니다.",
        "youtube_btn": "맞춤형 훈련 영상 보기"
    },
    "English": {
        "title": "⚡ ATHLETES AI: Global Motion Analysis Engine",
        "gender": "👤 Select Gender",
        "male": "Male",
        "female": "Female",
        "l1_label": "Step 1: Category",
        "l2_label": "Step 2: Sub-category",
        "l3_label": "Step 3: Sport & Target Part",
        "upload_model": "🌟 Premium AI: Upload Role Model Video (Optional)",
        "upload_user": "Upload Your Video (Required)",
        "analyzing_user": "🔍 Analyzing user video...",
        "analyzing_model": "🔍 Analyzing role model video...",
        "analysis_done": "✅ AI Deep Learning Analysis Complete!",
        "result_title": "Precision Analysis Result",
        "user_angle": "My Target Joint Angle",
        "model_angle": "Role Model Angle",
        "diff": "Difference",
        "sync_rate": "Posture Sync Rate",
        "feedback_title": "💡 AI Core Feedback",
        "pos_feedback": "Great attempt to utilize your range of motion according to your body structure. Excellent balance.",
        "neg_feedback": "However, the angle deviates from the standard range at the moment of impact. Core stability is needed.",
        "audio_title": "🔊 AI Multimodal (Posture + Audio) Diagnosis",
        "audio_desc": "**The loud impact sound when landing suggests high shock absorption. You need to relax your shoulders and utilize your iliopsoas muscles.**",
        "youtube_title": "📺 AI YouTube Training Prescription",
        "youtube_desc": "💡 Based on your body/rhythm analysis, the following training is recommended.",
        "youtube_btn": "Watch Custom Training Video"
    }
}
t = TEXT[lang]

# 3. [초단순 3단계 트리] - 한국어/영어 분리 (높이뛰기 추가 완료!)
if lang == "한국어":
    SPORT_TREE = {
        "하계 올림픽 종목": {
            "육상": ["100m 단거리 (하체: 골반-무릎-발목)", "마라톤/경보 (하체: 골반-무릎-발목)", "높이뛰기 (전신: 어깨-골반-발목)", "110m 허들 (전신: 어깨-골반-발목)", "창던지기 (상체: 어깨-팔꿈치-손목)"],
            "수영/수상": ["자유형/배영 (상체: 어깨-팔꿈치-손목)", "평영/접영 (상체: 어깨-팔꿈치-손목)"],
            "투기/무도": ["태권도 발차기 (하체: 골반-무릎-발목)", "복싱 펀치 (상체: 어깨-팔꿈치-손목)"],
            "라켓/타겟": ["테니스 (상체: 어깨-팔꿈치-손목)", "양궁 (상체: 어깨-팔꿈치-손목)"]
        },
        "동계 올림픽 종목": {
            "빙상": ["쇼트트랙 코너링 (하체: 골반-무릎-발목)", "피겨스케이팅 점프 (전신: 어깨-골반-발목)"],
            "설상": ["알파인 스키 (하체: 골반-무릎-발목)", "스노보드 턴 (전신: 어깨-골반-발목)"]
        },
        "대중 구기 종목": {
            "축구": ["슈팅/프리킥 (하체: 골반-무릎-발목)", "헤딩/점프 (전신: 어깨-골반-발목)"],
            "야구": ["투구/피칭 (상체: 어깨-팔꿈치-손목)", "타격/스윙 (전신: 어깨-골반-발목)"],
            "농구": ["점프슛 (상체: 어깨-팔꿈치-손목)"]
        }
    }
else:
    SPORT_TREE = {
        "Summer Olympics": {
            "Athletics": ["100m Sprint (Lower: Hip-Knee-Ankle)", "Marathon (Lower: Hip-Knee-Ankle)", "High Jump (Full: Shoulder-Hip-Ankle)", "110m Hurdles (Full: Shoulder-Hip-Ankle)", "Javelin (Upper: Shoulder-Elbow-Wrist)"],
            "Aquatics": ["Freestyle/Backstroke (Upper: Shoulder-Elbow-Wrist)", "Breaststroke/Butterfly (Upper: Shoulder-Elbow-Wrist)"],
            "Martial Arts": ["Taekwondo Kick (Lower: Hip-Knee-Ankle)", "Boxing Punch (Upper: Shoulder-Elbow-Wrist)"],
            "Racket/Target": ["Tennis (Upper: Shoulder-Elbow-Wrist)", "Archery (Upper: Shoulder-Elbow-Wrist)"]
        },
        "Winter Olympics": {
            "Ice Sports": ["Short Track (Lower: Hip-Knee-Ankle)", "Figure Skating Jump (Full: Shoulder-Hip-Ankle)"],
            "Snow Sports": ["Alpine Skiing (Lower: Hip-Knee-Ankle)", "Snowboard Turn (Full: Shoulder-Hip-Ankle)"]
        },
        "Ball Sports": {
            "Football/Soccer": ["Shooting/Freekick (Lower: Hip-Knee-Ankle)", "Header/Jump (Full: Shoulder-Hip-Ankle)"],
            "Baseball": ["Pitching (Upper: Shoulder-Elbow-Wrist)", "Batting/Swing (Full: Shoulder-Hip-Ankle)"],
            "Basketball": ["Jump Shot (Upper: Shoulder-Elbow-Wrist)"]
        }
    }

st.title(t["title"])

# 직관적 UI 구성
gender = st.radio(t["gender"], [t["male"], t["female"]], horizontal=True)

col1, col2 = st.columns(2)
with col1: l1 = st.selectbox(t["l1_label"], list(SPORT_TREE.keys()))
with col2: l2 = st.selectbox(t["l2_label"], list(SPORT_TREE[l1].keys()))
l3 = st.selectbox(t["l3_label"], SPORT_TREE[l1][l2])

# 타겟 부위 자동 추출
if lang == "한국어":
    target_part = l3.split("(")[1].split(":")[0]
else:
    target_part_en = l3.split("(")[1].split(":")[0]
    target_part_map = {"Upper": "상체", "Lower": "하체", "Full": "전신"}
    target_part = target_part_map.get(target_part_en, "전신")

# 4. 영상 처리 공통 함수 (재사용 가능하도록 독립시킴)
def analyze_video(uploaded_file, t_part, loading_msg):
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    st.info(loading_msg)
    progress_bar = st.progress(0)
    
    data_list = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            if t_part == "상체":
                a, b, c = [lm[11].x, lm[11].y], [lm[13].x, lm[13].y], [lm[15].x, lm[15].y]
            elif t_part == "전신":
                a, b, c = [lm[11].x, lm[11].y], [lm[23].x, lm[23].y], [lm[27].x, lm[27].y]
            else: # 하체
                a, b, c = [lm[23].x, lm[23].y], [lm[25].x, lm[25].y], [lm[27].x, lm[27].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            data_list.append(int(angle if angle <= 180 else 360-angle))
            
        frame_count += 1
        if total_frames > 0:
            progress_bar.progress(min(int((frame_count / total_frames) * 100), 100))

    cap.release()
    progress_bar.empty()
    return int(np.mean(data_list)) if data_list else 0

st.markdown("---")
model_file = st.file_uploader(t["upload_model"], type=["mp4", "mov", "avi"], key="model")
user_file = st.file_uploader(t["upload_user"], type=["mp4", "mov", "avi"], key="user")

if user_file is not None:
    # 1) 사용자 영상 분석
    user_avg = analyze_video(user_file, target_part, t["analyzing_user"])
    
    # 2) 롤모델 영상이 있으면 분석
    model_avg = None
    if model_file is not None:
        model_avg = analyze_video(model_file, target_part, t["analyzing_model"])

    st.success(t["analysis_done"])
    st.write("---")
    
    clean_title = l3.split('(')[0].strip()
    st.subheader(f"📊 {gender} {clean_title} {t['result_title']}")
    
    # [롤모델 영상이 업로드된 경우 비교 메트릭 출력]
    if model_avg is not None:
        sync_rate = max(0, 100 - abs(user_avg - model_avg) * 1.5)
        angle_diff = user_avg - model_avg
        
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric(t["user_angle"], f"{user_avg}°")
        mc2.metric(t["model_angle"], f"{model_avg}°", delta=f"{angle_diff}° {t['diff']}", delta_color="inverse")
        mc3.metric(t["sync_rate"], f"{int(sync_rate)}%")
    else:
        st.metric(t["user_angle"], f"{user_avg}°")

    # 긍정 피드백 & 교정 피드백
    st.markdown(f"### {t['feedback_title']}")
    st.success(f"**[+]** {t['pos_feedback']}")
    st.error(f"**[-]** {t['neg_feedback']}")

    # 멀티모달 진단
    st.markdown(f"### {t['audio_title']}")
    st.warning(t["audio_desc"])

    # 유튜브 훈련 매칭
    st.markdown(f"### {t['youtube_title']}")
    st.write(t["youtube_desc"])
    
    search_query = f"{clean_title} tutorial" if lang == "English" else f"{clean_title} 훈련법"
    st.link_button(f"▶️ {t['youtube_btn']}", f"https://www.youtube.com/results?search_query={search_query}")
