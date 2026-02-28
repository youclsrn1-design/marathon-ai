import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os
import webbrowser

# --- 1. AI 설정 ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    norm_ba = np.linalg.norm(ba); norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0: return 0
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    return int(np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0))))

ELITE_DB = {
    "마라톤": {"남성": {"Global": 174, "RoleModel": "엘리우드 킵초게"}, "여성": {"Global": 170, "RoleModel": "티지스트 아세파"}},
    "경보": {"남성": {"Global": 179, "RoleModel": "야마니시 토시카즈"}, "여성": {"Global": 178, "RoleModel": "양지유"}}
}

# --- 2. 리포트 생성 함수 ---
def get_advanced_report(sport, gender, user_angle):
    ref = ELITE_DB[sport][gender]["Global"]
    role_model = ELITE_DB[sport][gender]["RoleModel"]
    diff = user_angle - ref
    similarity = max(0, 100 - abs(diff) * 5)
    
    report = f"AI 분석 결과, 당신의 폼은 {role_model} 선수와 {similarity}% 일치합니다. "
    if sport == "마라톤":
        msg = "착지 시 충격 완화에 집중하세요." if diff > 5 else "추진 탄성이 좋습니다."
    else:
        msg = "무릎 펴기 규정에 유의하세요." if user_angle < 175 else "완벽한 보행입니다."
        
    return f"{report}\n\n[코칭 가이드]: {msg}", similarity

# --- 3. UI 구성 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("⚡ ATHLETES AI: 프리미엄 피드백 시스템")

with st.sidebar:
    st.header("💎 설정")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    user_email = "youclsrn1@gmail.com" # 선생님 이메일 고정
    st.write(f"📧 피드백 수신: {user_email}")

uploaded_file = st.file_uploader("분석할 영상을 업로드하세요", type=["mp4", "mov"])

if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out_path = "analyzed_final.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    angles = []
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
            cv2.putText(frame, f"{angle} deg", (int(p2[0]), int(p2[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        out.write(frame)
    cap.release(); out.release()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.video(out_path)
    with col2:
        user_peak = max(angles) if angles else 0
        report_text, score = get_advanced_report(sport, gender, user_peak)
        st.markdown(f"### 🏆 분석 결과\n{report_text}")
        
        # --- ✉️ 이메일 피드백 섹션 ---
        st.divider()
        st.subheader("📩 전문가 피드백 요청")
        user_message = st.text_area("AI 코치에게 궁금한 점을 적어주세요.", "이 자세에서 무릎 통증이 왜 생길까요?")
        
        # 메일 보내기 버튼 (컴퓨터의 기본 메일 앱을 띄웁니다)
        subject = f"[{sport}] AI 분석 피드백 요청 - {score}% 일치"
        body = f"분석결과: {user_peak}도\n내 질문: {user_message}"
        mailto_link = f"mailto:{user_email}?subject={subject}&body={body}"
        
        if st.button("이메일로 리포트 전송"):
            st.success(f"{user_email}로 전송할 준비가 되었습니다!")
            st.markdown(f'<a href="{mailto_link}" target="_blank">여기를 클릭하여 메일 앱 열기</a>', unsafe_allow_html=True)
