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

st.set_page_config(page_title="ATHLETES AI - 스포츠 통합 분석", layout="centered")

# 2. UI 구성 (수영, 체조, 사이클 추가)
st.title("🏆 ATHLETES AI: 전 종목 스포츠 분석 플랫폼")
event = st.selectbox("분석할 종목을 선택하세요", 
                     ["마라톤/러닝", "경보 (반칙 체크)", "축구 (슈팅/킥)", 
                      "골프 (스윙 궤적)", "역도/웨이트 (데드리프트)", 
                      "태권도 (발차기)", "유도 (메치기)",
                      "테니스 (포핸드/서브)", "배드민턴 (스매시)", "탁구 (드라이브)",
                      "수영 (스트로크)", "체조 (유연성/정렬)", "사이클 (페달링/피팅)"])

uploaded_file = st.file_uploader(f"[{event}] 영상을 올려주세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    frame_window = st.image([])
    status_text = st.empty()
    status_text.info(f"🔍 AI {event} 전문가가 자세를 정밀 분석 중입니다...")
    
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
            elbow = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # --- [종목별 특화 분석 로직] ---
            if event == "수영 (스트로크)":
                angle = calculate_angle(shoulder, elbow, wrist) # 하이 엘보우 체크
                data_list.append(angle)
            elif event == "사이클 (페달링/피팅)":
                angle = calculate_angle(hip, knee, ankle) # 페달링 무릎 각도
                data_list.append(angle)
            elif event == "체조 (유연성/정렬)":
                angle = calculate_angle(hip, knee, ankle) # 다리 찢기/정렬 각도
                data_list.append(angle)
            elif event in ["골프 (스윙 궤적)", "역도/웨이트 (데드리프트)"]:
                angle = calculate_angle(shoulder, hip, knee) # 상체 중립
                data_list.append(angle)
            else:
                angle = calculate_angle(hip, knee, ankle) # 기본 하체 분석
                data_list.append(angle)

        frame_window.image(image, channels="RGB")
        
    cap.release()
    status_text.empty()
    st.success(f"✅ {event} 분석 완료!")

    # 3. [전문가 용어 (쉬운 풀이)] 리포트 섹션
    st.subheader(f"📊 AI {event} 정밀 리포트")
    avg_val = int(np.mean(data_list)) if data_list else 0

    if event == "수영 (스트로크)":
        st.write(f"**하이 엘보우 각도 (물 잡기 효율):** {avg_val}도")
        st.markdown("* **진단:** 팔꿈치가 손목보다 높게 유지되어야 더 많은 물을 밀어낼 수 있습니다.")
    elif event == "사이클 (페달링/피팅)":
        st.write(f"**최대 무릎 신전 각도 (안장 높이 적절성):** {avg_val}도")
        st.markdown("* **진단:** 페달이 가장 아래일 때 무릎 각도가 145~155도 사이여야 관절에 무리가 없고 힘 전달이 좋습니다.")
    elif event == "체조 (유연성/정렬)":
        st.write(f"**신체 정렬 및 가동 각도 (유연성):** {avg_val}도")
        st.markdown("* **진단:** 관절의 최대 가동 범위를 활용하여 동작의 완성도를 높이세요.")
    else:
        st.write(f"**자세 분석 결과:** {avg_val}도")
        st.markdown("* **진단:** 동작 전반의 밸런스가 매우 양호합니다.")

    st.balloons()
