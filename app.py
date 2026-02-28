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
st.title("🏃‍♂️ ATHLETES AI: 초정밀 마라톤 & 경보 분석기")

# 🚨 사용자 주의사항 (대표님 요청)
st.warning("⚠️ **주의: 10초 이내의 영상만 올리세요.** (영상 분석 속도와 서버 안정성을 위함입니다)")

with st.sidebar:
    st.header("👤 분석 설정")
    sport = st.radio("종목 선택", ["마라톤", "경보"])
    gender = st.radio("성별", ["남성", "여성"])

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    # --- 상태 안내 (대표님 요청) ---
    status_placeholder = st.empty()
    status_placeholder.info("🔄 **업데이트 합니다...** (AI가 프레임 단위로 영상을 분석 중입니다)")
    
    try:
        # 입력 영상 처리
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # 출력 영상 경로 설정 (안전한 임시 경로 사용)
        out_tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        out_path = out_tfile.name
        
        # 코덱 설정 (웹 호환성이 높은 avc1 또는 mp4v 시도)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        angles = []
        foul_bent_frames = 0
        foul_flight_frames = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        progress_bar = st.progress(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)
            
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                lm = results.pose_landmarks.landmark
                
                hip = [lm[23].x * width, lm[23].y * height]
                knee = [lm[25].x * width, lm[25].y * height]
                ankle = [lm[27].x * width, lm[27].y * height]
                r_ankle = [lm[28].x * width, lm[28].y * height]
                
                angle = calculate_angle(hip, knee, ankle)
                angles.append(angle)
                
                if sport == "경보":
                    if angle < 170:
                        foul_bent_frames += 1
                        cv2.putText(frame, "KNEE BENT", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if lm[27].y < 0.85 and lm[28].y < 0.85:
                        foul_flight_frames += 1
                        cv2.putText(frame, "LOSS OF CONTACT", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
                cv2.putText(frame, f"Angle: {angle}", (int(knee[0]), int(knee[1])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            out.write(frame)
            if total_frames > 0:
                progress_bar.progress(min(len(angles) / total_frames, 1.0))

        cap.release()
        out.release()
        
        status_placeholder.empty()
        
        # 파일이 정상적으로 생성되었는지 확인 후 출력
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            st.success("✅ 분석 완료!")
            st.video(out_path)
        else:
            st.error("⚠️ **업데이트 합니다...** (영상 생성 실패. 코덱 호환성 문제입니다.)")
            
        # --- 리포트 출력 ---
        max_angle = max(angles) if angles else 0
        st.markdown(f"## 📊 {sport} 정밀 분석 결과")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("최대 무릎 신전 각도", f"{max_angle}°")
            
        with col2:
            if sport == "경보":
                st.subheader("🚨 AI 심판 판정")
                if foul_bent_frames > 3:
                    st.error(f"❌ 파울: 무릎 굽힘 감지 ({foul_bent_frames}회)")
                if foul_flight_frames > 3:
                    st.error(f"❌ 파울: 공중 부양 감지 ({foul_flight_frames}회)")
                if foul_bent_frames <= 3 and foul_flight_frames <= 3:
                    st.success("✅ Clean: 규정 위반 없음")
            else:
                st.subheader("🏃 마라톤 코칭")
                if max_angle > 170: st.success("훌륭한 자세입니다!")
                else: st.warning("무릎을 조금 더 펴서 보폭을 넓혀보세요.")

    except Exception as e:
        status_placeholder.error(f"⚠️ **업데이트 합니다...** (오류 발생: {e})")
