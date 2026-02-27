import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 및 유틸리티 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 각도 계산 함수 (관절 3개의 좌표로 각도 산출)
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360-angle
    return angle

st.set_page_config(page_title="ATHLETES AI - 종합 육상 분석", layout="centered")

# 2. UI 구성 (종목 선택 메뉴 추가)
st.title("🏆 ATHLETES AI: 육상 전 종목 통합 분석")
event = st.selectbox("분석할 종목을 선택하세요", 
                     ["마라톤/러닝", "경보 (Race Walking)", "단거리 (Sprints)", 
                      "창던지기/포환던지기", "높이뛰기/멀리뛰기", "허들"])

uploaded_file = st.file_uploader(f"[{event}] 영상을 올려주세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    frame_window = st.image([])
    status_text = st.empty()
    status_text.info(f"🔍 AI가 {event} 전용 로직으로 분석 중입니다...")
    
    analysis_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
            
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # 종목별 핵심 관절 추출
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # 뼈대 그리기
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # --- [종목별 핵심 로직] ---
            if event == "경보 (Race Walking)":
                angle = calculate_angle(hip, knee, ankle) # 무릎 펴짐 각도
                analysis_data.append(angle)
            elif event == "창던지기/포환던지기":
                angle = calculate_angle(shoulder, elbow, wrist) # 릴리즈 각도
                analysis_data.append(angle)
            elif event == "마라톤/러닝" or event == "단거리 (Sprints)":
                angle = calculate_angle(hip, knee, ankle)
                analysis_data.append(angle)
            else:
                analysis_data.append(knee[1]) # 기본값

        frame_window.image(image, channels="RGB")
        
    cap.release()
    status_text.empty()
    st.success(f"✅ {event} 분석 완료!")

    # 3. 종목별 맞춤형 '쉬운 용어' 리포트
    st.subheader(f"📊 {event} 정밀 진단 리포트")
    avg_val = np.mean(analysis_data) if analysis_data else 0

    if event == "경보 (Race Walking)":
        st.write(f"**평균 무릎 각도 (무릎 신전 유지):** {int(avg_val)}도")
        st.markdown("* **진단:** 착지 시 무릎이 180도에 가까울수록 반칙 위험이 적습니다.")
    elif event == "창던지기/포환던지기":
        st.write(f"**최대 팔 각도 (릴리즈 각도):** {int(avg_val)}도")
        st.markdown("* **진단:** 투척 시 팔의 각도가 45도 근처일 때 비거리가 극대화됩니다.")
    elif event == "마라톤/러닝":
        st.write(f"**무릎 신전 각도 (무릎 시원함):** {int(avg_val)}도")
        st.markdown("* **진단:** 다리가 뒤로 길게 뻗어지는지 확인하세요.")
    else:
        st.write("분석이 완료되었습니다. 자세 점수를 확인하세요.")

    st.balloons()
