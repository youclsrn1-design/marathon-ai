import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

# 1. MediaPipe 초기 세팅 (가장 가벼운 모델 사용)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# 2. 관절 각도 계산 함수 (핵심 AI 로직)
def calculate_angle(a, b, c):
    a = np.array(a) # 골반
    b = np.array(b) # 무릎
    c = np.array(c) # 발목
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# 3. Streamlit 웹 화면 구성
st.set_page_config(page_title="AI 육상/경보 코치", layout="wide")
st.title("🏃‍♂️ AI 육상 & 경보 파울 판독기")
st.write("무료 베타 버전입니다. 사진을 올리면 AI가 파울 여부를 즉시 판독합니다!")

# 4. 종목 선택 라디오 버튼
mode = st.radio("분석할 종목을 선택하세요:", ("마라톤 (자세 분석)", "경보 (파울 판독)"))

# 5. 이미지 업로드 기능 (동영상은 무료 서버가 터질 수 있어 일단 이미지로 MVP 검증)
uploaded_file = st.file_uploader("선수의 측면 전신 사진을 올려주세요 (jpg, png)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 이미지 읽기
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    
    # MediaPipe로 관절 분석
    results = pose.process(image_np)
    
    if results.pose_landmarks:
        # 뼈대 그리기
        annotated_image = image_np.copy()
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        # 경보 파울 판독 로직
        if mode == "경보 (파울 판독)":
            landmarks = results.pose_landmarks.landmark
            
            # 왼쪽 다리 관절 좌표 (측면이라고 가정)
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # 무릎 각도 계산
            knee_angle = calculate_angle(hip, knee, ankle)
            
            st.image(annotated_image, caption="AI 관절 분석 완료", use_container_width=True)
            
            # 파울 판정 결과 출력
            st.subheader("🚨 AI 심판 판독 결과")
            st.write(f"**현재 지지발(무릎) 각도:** {int(knee_angle)}도")
            
            if knee_angle < 160:
                st.error("⚠️ [파울] 무릎 굽힘 (Bent Knee) 규정 위반! \n\n 이유: 지지하는 다리의 무릎이 160도 미만으로 굽혀졌습니다. 무릎을 곧게 펴야 합니다.")
            else:
                st.success("✅ [통과] 완벽한 경보 자세입니다! 무릎이 잘 펴져 있습니다.")
                
        else:
            st.image(annotated_image, caption="마라톤 자세 분석 완료", use_container_width=True)
            st.success("안정적인 러닝 자세입니다. (마라톤 상세 분석 업데이트 예정)")
            
    else:
        st.warning("사람의 전신을 찾을 수 없습니다. 다른 사진을 올려주세요.")
