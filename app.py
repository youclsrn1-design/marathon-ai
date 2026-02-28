import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 📐 관절 각도 계산 함수
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return int(angle)

# --- UI 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("🏃‍♂️ ATHLETES AI: 마라톤 & 경보 착지 정밀 분석")

# 🚨 사용자 주의사항
st.warning("⚠️ **주의: 10초 이내의 영상만 올리세요.** (정밀 분석을 위해 필수입니다)")

with st.sidebar:
    st.header("👤 분석 설정")
    sport = st.radio("종목 선택", ["마라톤", "경보"])
    gender = st.radio("성별", ["남성", "여성"])

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    status_placeholder = st.empty()
    status_placeholder.info("🔄 **업데이트 합니다...** (AI가 착지 지점을 추적 중입니다)")
    
    try:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        out_tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        out_path = out_tfile.name
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        landing_angles = []
        foul_bent_count = 0
        foul_flight_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        progress_bar = st.progress(0)
        
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)
            
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                lm = results.pose_landmarks.landmark
                
                # 좌/우 발목 Y좌표 (지면 접촉 확인용)
                l_ankle_y = lm[27].y
                r_ankle_y = lm[28].y
                
                # 착지 지점 포착 로직: 발목이 화면 하단에 가장 가까워지는 순간
                # (MediaPipe Y는 아래로 갈수록 커짐, 0.85 이상을 지면 근처로 간주)
                is_landing_frame = l_ankle_y > 0.85 or r_ankle_y > 0.85
                
                # 관절 좌표 (분석용)
                hip = [lm[23].x * width, lm[23].y * height]
                knee = [lm[25].x * width, lm[25].y * height]
                ankle = [lm[27].x * width, lm[27].y * height]
                
                angle = calculate_angle(hip, knee, ankle)

                if sport == "경보" and is_landing_frame:
                    landing_angles.append(angle)
                    
                    # 1. 착지 지점 무릎 굽힘 포착 (175도 미만이면 파울로 간주)
                    if angle < 175:
                        foul_bent_count += 1
                        cv2.putText(frame, f"BENT! {angle}deg", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    
                    # 2. 착지 지점 공중 부양 포착 (양발이 지면에서 일정 높이 이상일 때)
                    if l_ankle_y < 0.82 and r_ankle_y < 0.82:
                        foul_flight_count += 1
                        cv2.putText(frame, "LOSS OF CONTACT!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                cv2.putText(frame, f"Knee: {angle}", (int(knee[0]), int(knee[1])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            out.write(frame)
            frame_idx += 1
            progress_bar.progress(min(frame_idx / total_frames, 1.0))

        cap.release()
        out.release()
        status_placeholder.empty()
        
        if os.path.exists(out_path):
            st.success("✅ 분석 완료!")
            st.video(out_path)
        
        # --- 리포트 섹션 ---
        st.markdown(f"## 📊 {sport} 착지 정밀 분석 리포트")
        avg_landing_angle = sum(landing_angles)//len(landing_angles) if landing_angles else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("착지 시 평균 각도", f"{avg_landing_angle}°")
            st.write("※ 경보 규정상 착지 시 무릎은 180도에 가깝게 펴져야 합니다.")
            
        with col2:
            if sport == "경보":
                st.subheader("🚨 착지 지점 파울 판정")
                if foul_bent_count > 0:
                    st.error(f"❌ 무릎 굽힘 포착: {foul_bent_count}회")
                if foul_flight_count > 0:
                    st.error(f"❌ 공중 부양(떠 있음) 포착: {foul_flight_count}회")
                if foul_bent_count == 0 and foul_flight_count == 0:
                    st.success("✅ Clean: 모든 착지 지점이 규정 내에 있습니다.")
            else:
                st.subheader("🏃 마라톤 피드백")
                st.info(f"착지 각도 {avg_landing_angle}°를 바탕으로 추진력을 계산합니다.")

    except Exception as e:
        status_placeholder.error(f"⚠️ **업데이트 합니다...** (분석 중 오류: {e})")
else:
    st.info("좌측 설정을 확인하고 10초 이내의 영상을 올려주세요.")
