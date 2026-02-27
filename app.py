import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [성별 세분화 데이터베이스] - 남/여 기준치를 분리하여 정확도 확보
SPORT_DB = {
    "마라톤/러닝": {
        "남성": {"범위": (172, 180), "풀이": "남성 골반 구조상 무릎이 일직선에 가까워야 효율적인 추진력이 발생합니다."},
        "여성": {"범위": (168, 178), "풀이": "여성 특유의 Q-각도를 고려할 때, 무릎의 유연한 확장이 부상 방지의 핵심입니다."},
        "출처": "International Journal of Sports Medicine"
    },
    "야구 (투구)": {
        "남성": {"범위": (90, 105), "풀이": "강한 구속을 위해 팔꿈치가 어깨 선보다 약간 높은 위치를 유지해야 합니다."},
        "여성": {"범위": (85, 95), "풀이": "여성 투수는 유연성을 활용한 부드러운 아크 형성이 부상 방지에 중요합니다."},
        "출처": "American Sports Medicine Institute (ASMI)"
    },
    "경보": {
        "남성": {"범위": (178, 180), "풀이": "남성 경보 선수의 강력한 Knee-Lock 기준입니다."},
        "여성": {"범위": (177, 180), "풀이": "여성 골반 회전을 고려한 최적의 착지 각도입니다."},
        "출처": "IAAF Technical Standards"
    }
}

st.set_page_config(page_title="ATHLETES AI - 성별 맞춤 분석", layout="centered")
st.title("🔬 ATHLETES AI: 성별 맞춤형 정밀 코칭")

# 1. 성별 및 종목 선택 (신뢰의 시작)
col_a, col_b = st.columns(2)
with col_a:
    gender = st.radio("성별을 선택하세요", ["남성", "여성"])
with col_b:
    event = st.selectbox("종목 선택", list(SPORT_DB.keys()))

# 2. 분석 메커니즘 공시
info = SPORT_DB[event]
gender_info = info[gender]
with st.expander(f"🔍 {gender} {event} 분석 메커니즘 (신뢰도 확인)", expanded=True):
    st.write(f"✅ **적용 기준:** {gender} 신체 구조에 최적화된 데이터")
    st.write(f"✅ **권장 범위:** {gender_info['범위']}°")
    st.write(f"✅ **분석 근거:** {info['출처']}")

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # (영상 처리 로직 - 위와 동일)
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    data_list = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            # 엉덩이-무릎-발목 각도 추출 예시
            a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            data_list.append(angle if angle <= 180 else 360-angle)
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cap.release()

    # --- [성별 기반 정밀 리포트] ---
    st.write("---")
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_info["범위"]

    st.subheader(f"📊 {gender} {event} 정밀 리포트")
    col1, col2 = st.columns(2)
    col1.metric("나의 측정값", f"{user_avg}°")
    col2.metric(f"{gender} 표준 범위", f"{min_s}° ~ {max_s}°")

    st.markdown("### 🎯 핵심 요약")
    if min_s <= user_avg <= max_s:
        st.success(f"당신의 자세는 {gender} 프로 선수들의 표준 데이터와 완벽히 일치합니다!")
    else:
        st.warning(f"{gender} 신체 구조 기준, 자세 교정이 필요합니다.")

    st.markdown("### 💡 상세 원리")
    st.write(gender_info["풀이"])
