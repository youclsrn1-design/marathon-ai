import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 및 유틸리티 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 각도 계산 함수 (관절 3개 포인트 활용)
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360-angle
    return angle

st.set_page_config(page_title="ATHLETES AI - 전 종목 분석", layout="centered")

# 2. UI 구성 (스포츠 카테고리 확장)
st.title("🏆 ATHLETES AI: 전 종목 스포츠 분석")
event = st.selectbox("분석할 스포츠를 선택하세요", 
                     ["마라톤/러닝", "경보 (반칙 체크)", "축구 (슈팅/킥)", 
                      "골프 (스윙 궤적)", "역도/웨이트 (데드리프트)", "투척/창던지기"])

uploaded_file = st.file_uploader(f"[{event}] 영상을 올려주세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    frame_window = st.image([])
    status_text = st.empty()
    status_text.info(f"🔍 AI {event} 전문가가 분석을 시작합니다...")
    
    data_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
            
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            
            # 주요 관절 좌표 (왼쪽 기준 예시)
            shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # 실시간 뼈대 그리기
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # --- [종목별 특화 분석 로직] ---
            if event == "경보 (반칙 체크)":
                angle = calculate_angle(hip, knee, ankle) # 무릎 펴짐
                data_list.append(angle)
            elif event == "골프 (스윙 궤적)":
                angle = calculate_angle(shoulder, hip, knee) # 척추 각도 유지
                data_list.append(angle)
            elif event == "축구 (슈팅/킥)":
                angle = calculate_angle(hip, knee, ankle) # 킥 임팩트 각도
                data_list.append(angle)
            elif event == "역도/웨이트 (데드리프트)":
                angle = calculate_angle(shoulder, hip, knee) # 등/허리 중립도
                data_list.append(angle)
            else:
                data_list.append(calculate_angle(hip, knee, ankle)) # 기본 하체 분석

        frame_window.image(image, channels="RGB")
        
    cap.release()
    status_text.empty()
    st.success(f"✅ {event} 분석 완료!")

    # 3. [전문가 용어 (쉬운 풀이)] 리포트 섹션
    st.subheader(f"📊 AI {event} 정밀 리포트")
    avg_val = int(np.mean(data_list)) if data_list else 0

    if event == "축구 (슈팅/킥)":
        st.write(f"**임팩트 시 무릎 각도:** {avg_val}도")
        st.markdown("* **진단:** 슈팅 시 무릎이 너무 일찍 펴지면 공이 위로 뜰 수 있습니다.")
    elif event == "골프 (스윙 궤적)":
        st.write(f"**척추 각 유지 (Spine Angle):** {avg_val}도")
        st.markdown("* **진단:** 스윙 도중 상체가 들리는 '헤드업' 현상을 체크하세요.")
    elif event == "역도/웨이트 (데드리프트)":
        st.write(f"**상체 중립도 (Back Neutrality):** {avg_val}도")
        st.markdown("* **진단:** 허리가 말리지 않고 일직선으로 잘 유지되는지 확인이 필요합니다.")
    elif event == "경보 (반칙 체크)":
        st.write(f"**무릎 신전 각도 (Knee Lock):** {avg_val}도")
        st.markdown("* **진단:** 180도에 가까워야 경보 규칙 위반(Bent Knee)을 피할 수 있습니다.")
    else:
        st.write(f"**핵심 분석 각도:** {avg_val}도")
        st.markdown("* **진단:** 전반적인 밸런스가 양호합니다.")

    st.balloons()
