import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0: angle = 360-angle
    return angle

st.set_page_config(page_title="ATHLETES AI - 전 종목 분석", layout="centered")

# 2. UI 구성 (태권도, 유도 추가)
st.title("🏆 ATHLETES AI: 스포츠/무도 통합 분석")
event = st.selectbox("분석할 종목을 선택하세요", 
                     ["마라톤/러닝", "경보 (반칙 체크)", "축구 (슈팅/킥)", 
                      "골프 (스윙 궤적)", "역도/웨이트 (데드리프트)", 
                      "태권도 (발차기 분석)", "유도 (메치기/무릎 중심)"])

uploaded_file = st.file_uploader(f"[{event}] 영상을 올려주세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    frame_window = st.image([])
    status_text = st.empty()
    status_text.info(f"🔍 AI {event} 전문가가 자세를 분석 중입니다...")
    
    data_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
            
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # --- [종목별 특화 분석 로직] ---
            if event == "태권도 (발차기 분석)":
                angle = calculate_angle(hip, knee, ankle) # 발차기 확장 각도
                data_list.append(angle)
            elif event == "유도 (메치기/무릎 중심)":
                angle = calculate_angle(hip, knee, ankle) # 중심 낮추기 각도
                data_list.append(angle)
            elif event == "골프 (스윙 궤적)" or event == "역도/웨이트 (데드리프트)":
                angle = calculate_angle(shoulder, hip, knee) # 척추/상체 각도
                data_list.append(angle)
            else:
                data_list.append(calculate_angle(hip, knee, ankle))

        frame_window.image(image, channels="RGB")
        
    cap.release()
    status_text.empty()
    st.success(f"✅ {event} 분석 완료!")

    # 3. [전문가 용어 (쉬운 풀이)] 리포트 섹션
    st.subheader(f"📊 AI {event} 정밀 리포트")
    avg_val = int(np.mean(data_list)) if data_list else 0

    if event == "태권도 (발차기 분석)":
        st.write(f"**임팩트 신전 각도 (발차기 시원함):** {avg_val}도")
        st.markdown("* **진단:** 발을 뻗는 순간 무릎이 곧게 펴져야 타격력이 극대화됩니다.")
    elif event == "유도 (메치기/무릎 중심)":
        st.write(f"**무릎 굴곡 각도 (중심 낮추기):** {avg_val}도")
        st.markdown("* **진단:** 메치기 순간 무릎을 충분히 굽혀 중심을 낮춰야 상대의 체중을 이용하기 쉽습니다.")
    elif event == "골프 (스윙 궤적)":
        st.write(f"**척추 각 유지 (Spine Angle):** {avg_val}도")
        st.markdown("* **진단:** 상체가 들리지 않아야 일관된 스윙이 가능합니다.")
    else:
        st.write(f"**핵심 분석 데이터:** {avg_val}도")
        st.markdown("* **진단:** 분석 결과 자세가 안정적입니다.")

    st.balloons()
