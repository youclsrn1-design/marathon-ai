import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
from datetime import datetime
import pandas as pd

# --- 1. AI 및 시각화 엔진 설정 ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    norm = (np.linalg.norm(ba) * np.linalg.norm(bc))
    if norm == 0: return 0
    cosine_angle = np.dot(ba, bc) / norm
    return int(np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0))))

ELITE_DB = {
    "마라톤": {"남성": {"Ref": 174, "Model": "엘리우드 킵초게"}, "여성": {"Ref": 170, "Model": "티지스트 아세파"}},
    "경보": {"남성": {"Ref": 179, "Model": "야마니시 토시카즈"}, "여성": {"Ref": 178, "Model": "양지유"}}
}

# --- 2. 기록 저장 및 리포트 ---
def save_log(name, contact, sport, angle):
    log_file = "usage_log.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([[now, name, contact, sport, angle]], columns=["시간", "이름", "연락처", "종목", "결과"])
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')

def get_supreme_report(sport, gender, user_angle):
    ref = ELITE_DB[sport][gender]["Ref"]
    model = ELITE_DB[sport][gender]["Model"]
    diff = user_angle - ref
    similarity = max(0, 100 - abs(diff) * 5)
    report = f"## 🏆 [AI Supreme 정밀 분석: {sport}]\n**롤모델:** {model} (싱크로율 {similarity}%)\n\n---\n"
    if sport == "마라톤":
        report += "⚠️ 교정: 오버스트라이드 억제를 위해 착지 보폭을 조절하세요.\n" if user_angle > ref + 3 else "✅ 양호: 탄성 유지가 훌륭합니다.\n"
    else: # 경보
        report += "⚠️ 교정: 'Bent Knee' 판정 위험! 착지 시 무릎을 더 펴세요.\n" if user_angle < 178 else "✅ 양호: 직선 보행 규정을 잘 준수 중입니다.\n"
    return report

# --- 3. UI 구성 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("⚡ ATHLETES AI: 통합 정밀 분석 시스템")

with st.sidebar:
    st.header("👤 사용자 등록")
    u_name = st.text_input("성함")
    u_contact = st.text_input("연락처")
    st.divider()
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov"])

if uploaded_file and u_name and u_contact:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    width, height, fps = int(cap.get(3)), int(cap.get(4)), cap.get(cv2.CAP_PROP_FPS)
    out_path = "final_output.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    angles = []
    bar = st.progress(0)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark
            p1, p2, p3 = [lm[23].x*width, lm[23].y*height], [lm[25].x*width, lm[25].y*height], [lm[27].x*width, lm[27].y*height]
            angle = calculate_precise_angle(p1, p2, p3)
            angles.append(angle)
            cv2.putText(frame, f"{angle}deg", (int(p2[0]), int(p2[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        out.write(frame)
        idx += 1
        if idx % 10 == 0: bar.progress(idx / total)
    cap.release(); out.release()
    col1, col2 = st.columns([2, 1])
    with col1: st.video(out_path)
    with col2:
        peak = max(angles) if angles else 0
        save_log(u_name, u_contact, sport, peak)
        st.success(f"✅ {u_name}님의 기록 저장 완료")
        st.markdown(get_supreme_report(sport, gender, peak))
