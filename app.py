import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os

# 1. AI 및 시각화 설정 (서버 에러 방지를 위해 complexity 1로 고정)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 📐 [수학] 관절 각도 계산용 물리 공식
# 관절 $B$를 꼭짓점으로 하는 두 벡터 $\vec{BA}$와 $\vec{BC}$ 사이의 사잇각 $\theta$를 구합니다.
# $$\theta = \arccos \left( \frac{\vec{BA} \cdot \vec{BC}}{|\vec{BA}| |\vec{BC}|} \right)$$
def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return int(angle)

# 📊 [엘리트 DB] 데이터 구조 최적화
ELITE_DB = {
    "마라톤": {
        "남성": {"Global": 173, "Korea": 170},
        "여성": {"Global": 169, "Korea": 166}
    },
    "경보": {
        "남성": {"Global": 179, "Korea": 178},
        "여성": {"Global": 178, "Korea": 177}
    }
}

# 🎙️ [Supreme 리포트 생성기]
def get_supreme_report(sport, gender, target, angle):
    # DB에서 기준 수치 안전하게 가져오기
    ref = ELITE_DB[sport][gender][target]
    diff = angle - ref
    
    report = f"### 📊 [AI 초정밀 역학 진단: {sport}]\n\n"
    report += f"**1. 수치 분석 (Fact Check)**\n측정된 피크 각도는 **{angle}°**입니다. {gender} {target} 엘리트 기준({ref}°) 대비 **{abs(diff)}° {'차이' if abs(diff)>2 else '일치'}**를 보입니다.\n\n"
    report += f"**2. 논리적 원인 분석 (Root Cause)**\n현재 각도는 지면 접촉 시 코어 근육의 개입이 늦어지는 현상을 보입니다. 이로 인해 추진 에너지가 지면으로 분산되고 있습니다.\n\n"
    
    metaphor = "마치 바람 빠진 공이 바닥에서 튀어 오르지 못하는 것과 같습니다." if diff < 0 else "마치 너무 딱딱한 나무 막대기가 부러지기 쉬운 상태와 같습니다."
    report += f"**3. 💡 AI 코치의 비유 (Metaphor)**\n{metaphor} 몸의 관절을 '강력한 용수철'이라 생각하세요.\n\n"
    report += f"> 🇺🇸 **Easy English:** Your knee angle is {angle}°. It should be straight like a ruler ({ref}°) at the impact. Use your leg like a 'Strong Spring'!"
    
    return report

# --- UI 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("⚡ ATHLETES AI: 실시간 시각화 & 정밀 분석")

with st.sidebar:
    st.header("👤 설정")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    target = st.radio("비교 대상", ["Global", "Korea"])

uploaded_file = st.file_uploader("분석할 영상을 업로드하세요", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # [오타 수정 완료] 괄호 및 중복 함수 제거
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out_path = "analyzed_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    angles = []
    st.info("🔍 AI가 뼈대를 추출하고 각도를 시각화 중입니다...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark
            p1 = [lm[23].x * width, lm[23].y * height]
            p2 = [lm[25].x * width, lm[25].y * height]
            p3 = [lm[27].x * width, lm[27].y * height]
            
            angle = calculate_precise_angle(p1, p2, p3)
            angles.append(angle)
            cv2.putText(frame, str(angle), (int(p2[0]), int(p2[1])), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)

    cap.release()
    out.release()
    
    st.video(out_path)
    user_peak = max(angles) if angles else 0
    st.markdown(get_supreme_report(sport, gender, target, user_peak))
