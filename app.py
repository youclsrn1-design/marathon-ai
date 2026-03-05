import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import os
from PIL import Image

# 화면 기본 설정
st.set_page_config(page_title="마라톤 AI", page_icon="🏃‍♂️", layout="wide")

st.title("🏃‍♂️ 마라톤 리얼 역학 분석 AI")
st.write("안전하고 과학적인 마라톤 완주부터 세계 제패까지, 맞춤형 AI 역학 분석")
st.warning("🔒 업로드된 모든 영상은 AI가 분석 후 임시 처리되어 즉시 소멸됩니다. 서버에 저장되지 않습니다.")

st.write("---")

# 1. 기본 정보 입력
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    gender = st.radio("1️⃣ 성별", ["남성", "여성"], horizontal=True)
with col_info2:
    region = st.radio("2️⃣ 기준", ["한국 기준", "글로벌 기준"], horizontal=True)
with col_info3:
    # 🔥 한국/글로벌 기준과 성별을 조합하여 목표를 세계 최고 수준으로 세분화!
    if region == "글로벌 기준":
        if gender == "남성":
            elite_label = "글로벌 엘리트 (2시간 05분 이내) 🌍"
        else:
            elite_label = "글로벌 엘리트 (2시간 15분 이내) 🌍"
    else:
        if gender == "남성":
            elite_label = "한국 엘리트 (2시간 15분 이내) 🇰🇷"
        else:
            elite_label = "한국 엘리트 (2시간 30분 이내) 🇰🇷"
            
    target_time = st.selectbox("3️⃣ 목표 기록", [elite_label, "서브 3", "서브 4", "완주 목표"])

st.write("---")

# 2. 달리기 영상 업로드
st.subheader("4️⃣ 달리기 분석 영상 업로드")
st.warning("⚠️ 안정적인 AI 분석을 위해 반드시 **10초 이내의 영상만 올려주세요!** (너무 긴 영상은 서버가 다운될 수 있습니다)")
uploaded_video = st.file_uploader("자세 분석을 위한 러닝 영상을 올려주세요 (MP4/MOV 추천)", type=['mp4', 'mov'])

st.write("---")

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

if uploaded_video is not None and st.button("실시간 역학 분석 및 처방 발급하기"):
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_video.read())
    tfile_path = tfile.name
    tfile.close()
    
    cap = cv2.VideoCapture(tfile_path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    touchdown_knee_angle = None
    touchdown_frame_pil = None
    trunk_lean_angle = None
    trunk_frame_pil = None
    
    # 지면에 가장 가까운 발목 위치를 찾기 위한 변수 (MediaPipe는 아래로 갈수록 Y값이 큽니다)
    max_ankle_y = 0.0 
    
    with st.spinner("AI가 영상을 프레임 단위로 쪼개어 정밀 역학 분석 중입니다. (임시 처리 후 즉시 소멸됩니다)"):
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            # 프레임 스킵을 줄여 착지 순간을 더 정밀하게 포착합니다 (기존 5 -> 2)
            if frame_count % 2 != 0:
                continue

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # 왼쪽 다리 좌표 추출
                l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                # 오른쪽 다리 좌표 추출
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # 현재 프레임에서 지면(아래)에 더 가까운 다리 찾기
                if l_ankle[1] > r_ankle[1]:
                    current_ankle_y = l_ankle[1]
                    current_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
                else:
                    current_ankle_y = r_ankle[1]
                    current_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
                
                # 여태까지 본 발목 위치 중 가장 지면에 가깝다면(착지 순간) 데이터 업데이트
                if current_ankle_y > max_ankle_y:
                    max_ankle_y = current_ankle_y
                    touchdown_knee_angle = current_knee_angle
                    
                    # 뼈대 그리기 및 이미지 저장
                    mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    touchdown_frame_pil = Image.fromarray(image_rgb)
                    
                    # 상체 기울기도 착지 순간을 기준으로 통일하여 측정
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    shoulder_vec = np.array(left_shoulder)
                    hip_vec = np.array(l_hip) # 왼쪽 힙을 기준으로 계산
                    lean_radians = np.arctan2(shoulder_vec[0]-hip_vec[0], shoulder_vec[1]-hip_vec[1])
                    trunk_lean_angle = np.abs(lean_radians * 180.0 / np.pi)
                    trunk_frame_pil = Image.fromarray(image_rgb)

        cap.release()
        pose.close()

    # 영상 즉시 소멸 
    try:
        os.unlink(tfile_path)
    except:
        pass

    if touchdown_frame_pil is not None:
        st.subheader(f"📐 [{region} / {gender}] AI 관절 각도 측정 결과")
        col1, col2 = st.columns(2)
        with col1:
            st.image(touchdown_frame_pil, caption=f"착지 순간 무릎 각도: {touchdown_knee_angle:.1f}도", use_column_width=True)
            st.write(f"💡 착지 시 무릎 각도: **{touchdown_knee_angle:.1f}도**")

        with col2:
            if trunk_frame_pil is not None:
                st.image(trunk_frame_pil, caption=f"상체 기울기: {trunk_lean_angle:.1f}도", use_column_width=True)
                st.write(f"💡 상체 기울기: **{trunk_lean_angle:.1f}도**")
        
        st.write("---")
        st.subheader("💊 [진짜] 역학 기반 맞춤형 처방전")
        
        # 글로벌 엘리트 vs 한국 엘리트를 구분하는 초정밀 역학 피드백
        if "글로벌 엘리트" in target_time:
            if touchdown_knee_angle > 140:
                st.error(f"⚠️ **[글로벌 톱클래스 경고 / 미세 제동력 발생]**\n\n**[역학 분석]** 세계 기록을 노리는 글로벌 스탠다드에서 무릎 각도 {touchdown_knee_angle:.1f}도는 치명적입니다. 무게 중심보다 미세하게 앞서 착지하며 러닝 이코노미가 손실되고 있습니다.\n\n**[월드클래스 처방]** 포어풋/미드풋 전환을 위한 카프바운딩 훈련을 극대화하고, 골반의 전방 회전을 더 활용하세요.")
            else:
                st.success(f"🔥 **[글로벌 톱클래스 통과 / 킵초게급 폼]**\n\n**[역학 분석]** 아프리카 최상위 선수들과 비견될 완벽한 텐션({touchdown_knee_angle:.1f}도)입니다. 지면 반발력을 100% 탄성에너지로 전환 중입니다.\n\n**[월드클래스 처방]** 세계 무대가 코앞입니다! 현재의 수직 진폭을 유지하세요.")
        elif "한국 엘리트" in target_time:
            if touchdown_knee_angle > 142:
                st.error(f"⚠️ **[국내 엘리트 경고 / 오버스트라이딩 주의]**\n\n**[역학 분석]** 국내 정상급 기록을 위해선 더 강한 추진력이 필요하지만, 현재 각도({touchdown_knee_angle:.1f}도)는 보폭을 억지로 늘리려다 발생하는 전형적인 브레이킹 모션입니다.\n\n**[국내 엘리트 처방]** 억지로 보폭을 늘리지 말고, 케이던스를 185 이상으로 높여 착지점을 몸쪽으로 당기세요.")
            else:
                st.success(f"🔥 **[국내 엘리트 통과 / 안정적인 효율]**\n\n**[역학 분석]** 무릎 각도가 {touchdown_knee_angle:.1f}도로 매우 효율적인 텐션을 유지하고 있습니다.\n\n**[국내 엘리트 처방]** 훌륭합니다! 이 효율을 바탕으로 후반 30km 이후의 스태미나 훈련에 집중하세요.")
        else:
            if touchdown_knee_angle > 145:
                st.error(f"⚠️ **[{target_time} 목표 / 무릎 충격 과다 위험]** 착지 시 무릎이 너무 펴져 있습니다(오버스트라이딩).\n\n**[역학적 분석]** 지면의 충격이 무릎 관절로 고스란히 전달됩니다. (장경인대/무릎 연골 손상 위험)\n\n**[처방]** 보폭을 살짝 줄이고, 몸 바로 아래에 발을 딛는 연습을 하세요.")
            elif touchdown_knee_angle < 135:
                st.warning(f"⚡ **[{target_time} 목표 / 추진력 손실 주의]** 무릎이 다소 굽혀져 착지합니다.\n\n**[역학적 분석]** 근육 에너지를 과도하게 쓰게 되어 후반 페이스가 처질 수 있습니다.\n\n**[처방]** 런지, 스쿼트로 하체 지지력을 키우세요.")
            else:
                st.success(f"🔥 **[{target_time} 목표 / 안정적인 자세]** 아주 훌륭한 착지 자세입니다. 현재 각도를 유지하세요!")
            
        st.write("---")
        st.success("✅ 분석 완료 후 업로드된 영상은 임시 처리되어 즉시 소멸되었습니다.")
    else:
        st.error("⚠️ 영상에서 자세를 인식하지 못했습니다. 전신이 잘 보이는 영상을 업로드해 주세요!")

# 대표님 이메일 피드백 안내 (화면 맨 아래에 추가)
st.write("---")
st.info("💡 **서비스 개선을 위한 소중한 의견을 들려주세요!**\n\n버그 신고, 기능 제안 등 어떤 피드백이든 환영합니다. 아래 이메일로 연락해 주세요.\n\n📧 **[youclsrn1@gmail.com](mailto:youclsrn1@gmail.com)**")
