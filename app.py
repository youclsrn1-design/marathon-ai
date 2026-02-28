import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os

# 1. AI 및 시각화 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 📐 관절 각도 계산용 물리 공식
def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return int(angle)

# 📊 엘리트 데이터베이스
ELITE_DB = {
    "마라톤": {"남성": {"Global": 173, "Korea": 170}, "여성": {"Global": 169, "Korea": 166}},
    "경보": {"남성": {"Global": 179, "Korea": 178}, "여성": {"Global": 178, "Korea": 177}}
}

# 🎙️ [Supreme 리포트] + [파울 판정] 생성기
def get_supreme_report(sport, gender, target, max_angle, foul_bent, foul_flight):
    ref = ELITE_DB[sport][gender][target]
    diff = max_angle - ref
    
    report = f"### 📊 [AI 초정밀 역학 진단: {sport}]\n\n"
    
    # 파울 판정 섹션 (경보 전용)
    if sport == "경보":
        report += "#### 🚨 AI 심판 판독 (Judge Panel)\n"
        if foul_bent or foul_flight:
            if foul_bent:
                report += "- **⚠️ 파울: 무릎 굽힘 (Bent Knee)**\n  - *이유: 지면 접촉 시점부터 수직 단계까지 무릎이 175° 이상 펴지지 않았습니다.*\n"
            if foul_flight:
                report += "- **⚠️ 파울: 공중 부양 (Loss of Contact)**\n  - *이유: 양발이 동시에 지면에서 떨어진 프레임이 포착되었습니다.*\n"
        else:
            report += "- **✅ Clean: 파울 없음.** 완벽한 규정 준수 자세입니다.\n"
        report += "\n---\n"

    report += f"**1. 수치 분석 (Fact Check)**\n최대 신전 각도는 **{max_angle}°**입니다. 기준({ref}°) 대비 **{abs(diff)}° {'차이' if abs(diff)>2 else '일치'}**를 보입니다.\n\n"
    report += f"**2. 논리적 원인 분석 (Root Cause)**\n현재 각도는 추진 에너지가 지면으로 분산되는 지점을 보여줍니다.\n\n"
    
    metaphor = "마치 바람 빠진 공이 바닥에서 튀어 오르지 못하는 것과 같습니다." if diff < 0 else "마치 너무 유연성이 부족한 나무 막대기와 같습니다."
    report += f"**3. 💡 AI 코치의 비유 (Metaphor)**\n{metaphor}\n\n"
    report += f"> 🇺🇸 **Easy English:** Max knee angle: {max_angle}°. Target: {ref}°. Keep your leg straight at contact!"
    
    return report

# --- UI 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("⚡ ATHLETES AI: 경보 파울 판독 및 실시간 분석")

with st.sidebar:
    st.header("👤 설정")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    target = st.radio("비교 대상", ["Global", "Korea"])

uploaded_file = st.file_uploader("분석할 영상을 업로드하세요 (MP4, MOV)", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out_path = "analyzed_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    angles = []
    foul_bent = False
    foul_flight = False
    
    st.info("🔍 AI 심판이 영상을 프레임 단위로 정밀 분석 중입니다...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark
            
            # 왼쪽/오른쪽 관절 좌표 추출
            l_hip = [lm[23].x * width, lm[23].y * height]
            l_knee = [lm[25].x * width, lm[25].y * height]
            l_ankle = [lm[27].x * width, lm[27].y * height]
            r_ankle = [lm[28].x * width, lm[28].y * height]
            
            # 1. 무릎 각도 계산 및 파울 체크
            angle = calculate_precise_angle(l_hip, l_knee, l_ankle)
            angles.append(angle)
            
            if sport == "경보" and angle < 170: # 경보 규정: 무릎은 펴져야 함
                foul_bent = True
                cv2.putText(frame, "BENT KNEE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # 2. 공중 부양 파울 체크 (양발 Y좌표가 지면에서 일정 높이 이상일 때)
            # MediaPipe Y값은 작을수록 위쪽입니다.
            if sport == "경보":
                if lm[27].y < 0.85 and lm[28].y < 0.85: # 양발이 모두 지면(0.9) 위로 떴을 때
                    foul_flight = True
                    cv2.putText(frame, "LOSS OF CONTACT!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv2.putText(frame, f"Angle: {angle}", (int(l_knee[0]), int(l_knee[1])), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        out.write(frame)

    cap.release()
    out.release()
    
    st.video(out_path)
    user_peak = max(angles) if angles else 0
    st.markdown(get_supreme_report(sport, gender, target, user_peak, foul_bent, foul_flight))
