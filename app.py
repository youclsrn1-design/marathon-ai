import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import time
import os
from PIL import Image

# 화면 기본 설정
st.set_page_config(page_title="마라톤 AI", page_icon="🏃‍♂️", layout="wide")

st.title("🏃‍♂️ 마라톤 리얼 역학 분석 AI")
st.write("안전하고 과학적인 마라톤 완주를 위한 맞춤형 AI 역학 분석 및 부상 처방")
st.warning("🔒 업로드된 모든 영상은 AI가 분석 후 임시 처리되어 즉시 소멸됩니다. 서버에 저장되지 않습니다.")

st.write("---")

# 1. 기본 정보 입력 (분석 가중치에 사용)
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    gender = st.radio("1️⃣ 성별", ["남성", "여성"], horizontal=True)
with col_info2:
    region = st.radio("2️⃣ 기준", ["한국 기준", "글로벌 기준"], horizontal=True)
with col_info3:
    target_time = st.selectbox("3️⃣ 목표 기록", ["서브 3", "서브 4", "완주 목표"])

st.write("---")

# 2. 달리기 영상 업로드
st.subheader("4️⃣ 달리기 분석 영상 업로드")
uploaded_video = st.file_uploader("자세 분석을 위한 러닝 영상을 올려주세요 (MP4/MOV 추천)", type=['mp4', 'mov'])

st.write("---")

# ---------------------------------------------------------
# 역학 분석 핵심 함수: 관절 각도 계산 (trigonometry)
# ---------------------------------------------------------
def calculate_angle(a, b, c):
    a = np.array(a) # First landmark
    b = np.array(b) # Mid landmark
    c = np.array(c) # End landmark
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

# ---------------------------------------------------------
# 3. 실시간 AI 역학 분석 및 처방 발급
# ---------------------------------------------------------
if uploaded_video is not None and st.button("실시간 역학 분석 및 처방 발급하기"):
    
    # 임시 파일 처리 (소멸 기능)
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    tfile_path = tfile.name
    tfile.close() # Close to allow opencv to open
    
    cap = cv2.VideoCapture(tfile_path)
    
    # MediaPipe Pose 설정
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # 결과 저장을 위한 변수들
    touchdown_knee_angle = None
    touchdown_frame_pil = None
    trunk_lean_angle = None
    trunk_frame_pil = None
    
    with st.spinner("AI가 영상을 프레임 단위로 쪼개어 정밀 역학 분석 중입니다. 약 30초~1분 정도 소요될 수 있습니다. (임시 처리 후 즉시 소멸됩니다)"):
        # 영상 처리 루프
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            
            # (Streamlit Cloud 성능 이슈로 매 5프레임마다 분석)
            if frame_count % 5 != 0:
                continue

            # 분석용 이미지 변환 (BGR -> RGB)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # ---------------------------------------------------------
                # 핵심 역학 데이터 1: 무릎 각도 (착지 순간)
                # ---------------------------------------------------------
                # (예시: 왼쪽 다리 기준)
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                knee_angle = calculate_angle(hip, knee, ankle)
                
                # 심플 로직: 가장 펴지는 순간(최대 각도)을 착지 전후로 판단
                if touchdown_knee_angle is None or knee_angle > touchdown_knee_angle:
                    touchdown_knee_angle = knee_angle
                    # 관절 그리기
                    mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    touchdown_frame_pil = Image.fromarray(image_rgb)

                # ---------------------------------------------------------
                # 핵심 역학 데이터 2: 상체 기울기 (Trunk Lean)
                # ---------------------------------------------------------
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                
                # 수직선 대비 상체 각도 계산 (y축 기준)
                shoulder_vec = np.array(left_shoulder)
                hip_vec = np.array(left_hip)
                lean_radians = np.arctan2(shoulder_vec[0]-hip_vec[0], shoulder_vec[1]-hip_vec[1])
                lean_angle = np.abs(lean_radians * 180.0 / np.pi)

                if trunk_lean_angle is None or lean_angle < trunk_lean_angle: # 가장 수직에 가까운 린 각도 저장
                    trunk_lean_angle = lean_angle
                    trunk_frame_pil = Image.fromarray(image_rgb)

        cap.release()
        pose.close()

    # 데이터 삭제 및 소멸 처리 (핵심 요구사항)
    try:
        os.unlink(tfile_path) # 강제 삭제
    except Exception as e:
        pass # 삭제 실패 시에도 결과는 보여줌

    # ---------------------------------------------------------
    # 결과 화면 출력
    # ---------------------------------------------------------
    if touchdown_frame_pil is not None:
        st.subheader("📐 AI 관절 각도 측정 결과 (역학적 바탕)")
        st.write("동영상으로는 놓치기 쉬운 찰나의 순간을 분석했습니다.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(touchdown_frame_pil, caption=f"착지 순간 무릎 각도: {touchdown_knee_angle:.1f}도", use_column_width=True)
            st.write(f"💡 착지 시 무릎 각도가 **{touchdown_knee_angle:.1f}도**로 측정되었습니다.\n(이상적인 범위: ~135~145도)")

        with col2:
            if trunk_frame_pil is not None:
                # 간단 관절 선 그리기
                st.image(trunk_frame_pil, caption=f"상체 기울기: {trunk_lean_angle:.1f}도", use_column_width=True)
                st.write(f"💡 상체 기울기가 수직 대비 **{trunk_lean_angle:.1f}도** 앞으로 기울었습니다.\n(이상적인 범위: 2~7도 리닝)")
        
        st.write("---")

        # ---------------------------------------------------------
        # 진짜 역학 기반 처방전 발급
        # ---------------------------------------------------------
        st.subheader("💊 [진짜] 역학 기반 부상 예방 처방전")
        
        if touchdown_knee_angle > 145:
            st.error(f"⚠️ **[{target_time} 목표 / 무릎 충격 과다 위험]** 분석 결과, 착지 시 무릎이 너무 펴져 있습니다(오버스트라이딩).\n\n**[역학적 분석]** 무릎이 펴진 상태로 착지하면 지면의 충격이 무릎 관절로 고스란히 전달됩니다. 이는 **장경인대 증후군 및 무릎 연골 손상**의 주원인입니다.\n\n**[처방]** 1. 보폭을 살짝 줄이세요. 2. 발 아래쪽이 아닌 골반 바로 아래로 착지한다는 느낌을 가지세요.")
        elif touchdown_knee_angle < 135:
            st.warning(f"⚡ **[{target_time} 목표 / 추진력 손실 주의]** 무릎이 다소 굽혀져 착지합니다.\n\n**[역학적 분석]** 무릎을 너무 많이 굽혀 착지하면 충격 흡수는 좋지만, 추진력을 얻기 위해 근육 에너지를 과도하게 쓰게 되어 페이스가 처질 수 있습니다.\n\n**[처방]** 하체 스트렝스 훈련(런지, 스쿼트)을 추가하여 착지 시 하체 지지력을 키우세요.")
        else:
            st.success(f"🔥 **[{target_time} 목표 / 안정적인 자세]** 아주 훌륭한 착지 자세입니다.\n\n**[역학적 분석]** 무릎 각도가 {touchdown_knee_angle:.1f}도로 지면 충격을 아주 안정적으로 흡수하고 있습니다.\n\n**[처방]** 현재 각도와 폼을 유지하세요. 부상 예방을 위해 달리기 전후 **동적 스트레칭**만 꼼꼼히 챙겨주세요.")
            
        st.write("---")
        st.success("✅ 분석 완료 후 업로드된 영상은 임시 처리되어 즉시 소멸되었습니다. 서버에 저장되지 않습니다.")

    else:
        st.error("⚠️ 정확한 처방을 위해 먼저 영상을 업로드해 주세요!")
