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
    
    max_ankle_y = 0.0 
    
    with st.spinner("AI가 영상을 프레임 단위로 쪼개어 정밀 역학 분석 중입니다. (임시 처리 후 즉시 소멸됩니다)"):
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            if frame_count % 2 != 0:
                continue

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                if l_ankle[1] > r_ankle[1]:
                    current_ankle_y = l_ankle[1]
                    current_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
                else:
                    current_ankle_y = r_ankle[1]
                    current_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
                
                if current_ankle_y > max_ankle_y:
                    max_ankle_y = current_ankle_y
                    touchdown_knee_angle = current_knee_angle
                    
                    mp_drawing.draw_landmarks(image_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    touchdown_frame_pil = Image.fromarray(image_rgb)
                    
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    shoulder_vec = np.array(left_shoulder)
                    hip_vec = np.array(l_hip)
                    lean_radians = np.arctan2(shoulder_vec[0]-hip_vec[0], shoulder_vec[1]-hip_vec[1])
                    trunk_lean_angle = np.abs(lean_radians * 180.0 / np.pi)
                    trunk_frame_pil = Image.fromarray(image_rgb)

        cap.release()
        pose.close()

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
        
        # 1. 상체 기울기 피드백 (기준 완화: 160도 ~ 175도)
        if trunk_lean_angle is not None:
            if 160 <= trunk_lean_angle <= 175:
                lean_feedback = "상체 전방 기울기(약 5~20도)가 추진력을 얻고 충격을 분산하기에 가장 이상적인 각도입니다."
            elif trunk_lean_angle < 160:
                lean_feedback = "상체가 너무 앞으로 숙여져 있습니다. 고관절이 펴지지 않아 보폭이 좁아질 수 있습니다."
            else:
                lean_feedback = "상체가 너무 세워져 있습니다(뒤로 젖혀짐). 무게중심이 뒤에 남아 브레이킹이 걸립니다."
            st.info(f"💡 **상체 밸런스 진단:** {lean_feedback}")

        # 2. 무릎 각도 피드백 
        if touchdown_knee_angle > 165:
            st.error(f"⚠️ **[오버스트라이딩 경고 / 무릎 충격 과다 위험]**\n\n**[역학 분석]** 착지 시 무릎 각도({touchdown_knee_angle:.1f}도)가 너무 펴져 있습니다. 몸의 무게 중심보다 한참 앞에서 발이 떨어지며 심각한 제동(Braking)이 걸리고 있습니다.\n\n**[처방]** 발을 멀리 뻗으려는 의식을 버리고, 케이던스(발구름 수)를 5~10% 높여 발이 몸(골반) 바로 아래에 떨어지도록 교정하세요. 장경인대염, 무릎 연골 부상을 유발하는 1순위 자세입니다.")
            
        elif touchdown_knee_angle < 145:
            st.warning(f"⚡ **[스태미나 고갈 주의 / 과도한 무릎 굽힘]**\n\n**[역학 분석]** 무릎이 {touchdown_knee_angle:.1f}도로 지나치게 굽혀진 상태에서 착지하고 있습니다. 일명 '그루초 달리기(Groucho running)' 폼으로, 뼈와 건의 탄성을 쓰지 못하고 대퇴사두근(허벅지 앞)의 근력만으로 체중을 버티고 있습니다.\n\n**[처방]** 후반 30km 이후 허벅지에 쥐가 날 확률이 매우 높습니다. 지면을 차고 나갈 때 골반을 조금 더 높게 들고 뛰는(수직 진폭을 살짝 높이는) 느낌을 가져가세요.")
            
        else:
            if "엘리트" in target_time:
                st.success(f"🔥 **[엘리트 폼 완벽 통과 / 최고의 러닝 이코노미]**\n\n**[역학 분석]** 엘리트 선수들의 완벽한 착지 각도({touchdown_knee_angle:.1f}도)입니다. 지면의 충격을 아킬레스건과 종아리의 탄성에너지로 100% 흡수 및 전환하고 있습니다.\n\n**[처방]** 무릎의 텐션과 롤링이 아프리카 최상위권 선수들과 비견될 만큼 훌륭합니다. 현재의 폼을 강력한 무기로 삼아 스피드 인터벌 훈련에 집중하세요!")
            else:
                st.success(f"🔥 **[{target_time} 통과 / 안정적이고 부상 없는 자세]**\n\n**[역학 분석]** 이상적인 무릎 굽힘({touchdown_knee_angle:.1f}도)을 통해 지면 충격을 부드럽게 흡수하는 완벽한 미드풋/포어풋 역학을 보여주고 있습니다.\n\n**[처방]** 부상 위험이 가장 적은 훌륭한 폼입니다! 이 효율적인 역학 밸런스를 믿고 마일리지(주간 달리기 거리)를 자신 있게 늘려가셔도 좋습니다.")
            
        st.write("---")
        st.success("✅ 분석 완료 후 업로드된 영상은 임시 처리되어 즉시 소멸되었습니다.")
    else:
        st.error("⚠️ 영상에서 자세를 인식하지 못했습니다. 전신이 잘 보이는 영상을 업로드해 주세요!")

# 대표님 이메일 피드백 안내
st.write("---")
st.info("💡 **서비스 개선을 위한 소중한 의견을 들려주세요!**\n\n버그 신고, 기능 제안 등 어떤 피드백이든 환영합니다. 아래 이메일로 연락해 주세요.\n\n📧 **[youclsrn1@gmail.com](mailto:youclsrn1@gmail.com)**")
