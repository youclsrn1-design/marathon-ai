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

# --- UI 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("🏃‍♂️ ATHLETES AI: 경보 지면 접촉 정밀 판독")

# 🚨 사용자 주의사항
st.warning("⚠️ **주의: 10초 이내의 영상만 올리세요.** (정밀 판독을 위해 필수입니다)")

with st.sidebar:
    st.header("👤 분석 설정")
    sport = st.radio("종목 선택", ["마라톤", "경보"])
    gender = st.radio("성별", ["남성", "여성"])

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file:
    status_placeholder = st.empty()
    status_placeholder.info("🔄 **업데이트 합니다...** (AI가 발의 지면 접촉 상태를 분석 중입니다)")
    
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

        foul_flight_frames = [] # 파울이 발생한 프레임 번호 저장
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
                
                # 좌/우 발목 및 발가락 Y좌표 (지면 접촉 확인용)
                # MediaPipe Y값은 1.0에 가까울수록 지면(아래쪽)입니다.
                l_foot = lm[27].y  # 왼쪽 발목
                r_foot = lm[28].y  # 오른쪽 발목
                
                # --- [경보 핵심 로직] 공중 부양(Loss of Contact) 판정 ---
                # 양발이 모두 특정 기준선(예: 0.82) 위로 올라가면 지면 이탈로 간주
                if sport == "경보":
                    if l_foot < 0.82 and r_foot < 0.82:
                        foul_flight_frames.append(frame_idx)
                        cv2.putText(frame, "LOSS OF CONTACT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                        # 발 주위에 경고 표시
                        cv2.circle(frame, (int(lm[27].x * width), int(lm[27].y * height)), 20, (0, 0, 255), -1)
                        cv2.circle(frame, (int(lm[28].x * width), int(lm[28].y * height)), 20, (0, 0, 255), -1)

            out.write(frame)
            frame_idx += 1
            if total_frames > 0:
                progress_bar.progress(min(frame_idx / total_frames, 1.0))

        cap.release()
        out.release()
        status_placeholder.empty()
        
        if os.path.exists(out_path):
            st.success("✅ 분석 완료!")
            st.video(out_path)
        
        # --- 리포트 섹션 ---
        st.markdown(f"## 📊 {sport} 판독 리포트")
        
        if sport == "경보":
            st.subheader("🚨 실시간 지면 접촉 판정")
            if len(foul_flight_frames) > 0:
                st.error(f"❌ **파울 감지:** 양발이 지면에서 동시에 떨어진 순간이 {len(foul_flight_frames)}프레임 포착되었습니다.")
                st.write("경보 규정상 한쪽 발은 항상 지면에 닿아 있어야 합니다. 현재 영상에서는 '뛰는 동작'이 감지되었습니다.")
            else:
                st.success("✅ **Clean:** 모든 구간에서 지면 접촉이 정상적으로 유지되었습니다.")
        else:
            st.info("마라톤 모드에서는 전신 밸런스와 주법을 중심으로 분석합니다. (업데이트 예정)")

    except Exception as e:
        status_placeholder.error(f"⚠️ **업데이트 합니다...** (분석 중 오류 발생: {e})")
else:
    st.info("좌측에서 종목을 선택하고 10초 이내의 영상을 올려주세요.")
