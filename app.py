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

# [정밀 역학] 관절 사잇각 계산 함수
def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0: return 0
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    return int(np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0))))

# 엘리트 데이터베이스
ELITE_DB = {
    "마라톤": {"남성": 174, "여성": 170},
    "경보": {"남성": 179, "여성": 178}
}

# --- 2. 기록 저장 함수 (CSV 로그) ---
def save_usage_log(name, contact, sport, angle):
    log_file = "usage_log.csv"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 새로운 데이터 행
    new_data = pd.DataFrame([[now, name, contact, sport, angle]], 
                            columns=["시간", "이름", "연락처", "종목", "결과각도"])
    
    # 파일이 없으면 새로 만들고, 있으면 이어쓰기
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False, encoding='utf-8-sig')

# --- 3. 정밀 분석 리포트 생성기 ---
def get_precision_report(sport, gender, user_angle):
    ref = ELITE_DB[sport][gender]
    diff = user_angle - ref
    
    report = f"## 📊 {sport} 정밀 분석 리포트\n\n"
    
    if abs(diff) <= 2:
        report += "⭐ **상태:** 최상급(Elite). 완벽한 역학 구조를 보입니다.\n\n"
    elif abs(diff) <= 5:
        report += "✅ **상태:** 양호(Good). 미세한 조정이 권장됩니다.\n\n"
    else:
        report += "⚠️ **상태:** 분석 필요(Caution). 자세 교정이 시급합니다.\n\n"

    report += "### 💡 전문 코칭 피드백\n"
    if sport == "마라톤":
        if user_angle > ref + 3:
            report += "* **현상:** 착지 시 무릎이 과하게 펴지는 '오버스트라이드'\n"
            report += "* **교정:** 보폭을 줄여 지면 충격을 흡수하세요.\n"
        else:
            report += "* **현상:** 무릎 굴곡이 깊어 에너지 분산 발생\n"
            report += "* **교정:** 지면 반발력을 더 활용해 보세요.\n"
    else: # 경보
        if user_angle < 178:
            report += "* **현상:** 'Bent Knee' 규정 위반 위험 감지\n"
            report += "* **교정:** 착지 시 무릎을 완벽히 펴야 합니다.\n"
        else:
            report += "* **현상:** 규정에 부합하는 우수한 직선 보행\n"
            report += "* **교정:** 골반 회전 가동범위를 더 넓혀보세요.\n"
            
    return report

# --- 4. UI/UX 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI: Precision Analysis", layout="wide")
st.title("🏃 ATHLETES AI: 마라톤 & 경보 정밀 분석")

# 사이드바: 사용자 정보 입력 및 설정
with st.sidebar:
    st.header("👤 사용자 정보")
    user_name = st.text_input("성함", placeholder="예: 홍길동")
    user_contact = st.text_input("연락처", placeholder="010-0000-0000")
    
    st.divider()
    st.header("⚙️ 분석 설정")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    
    st.divider()
    st.info("문의: youclsrn1@gmail.com")

# 파일 업로드
uploaded_file = st.file_uploader("분석할 훈련 영상을 업로드하세요", type=["mp4", "mov"])

if uploaded_file:
    # 1. 정보 입력 확인
    if not user_name or not user_contact:
        st.error("⚠️ 분석을 시작하려면 사이드바에 **이름과 연락처**를 먼저 입력해 주세요!")
    else:
        # 2. 영상 처리
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        out_path = "temp_analysis.mp4"
        out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        angles = []
        progress_bar = st.progress(0)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        frame_idx = 0
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
                cv2.putText(frame, f"{angle}deg", (int(p2[0]), int(p2[1])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            out.write(frame)
            frame_idx += 1
            if frame_idx % 10 == 0: progress_bar.progress(frame_idx / total_frames)
            
        cap.release(); out.release()

        # 3. 결과 출력 및 기록 저장
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("🎥 시각화 분석 결과")
            st.video(out_path)
        with col2:
            user_peak = max(angles) if angles else 0
            
            # 분석 완료 즉시 서버 CSV에 저장
            save_usage_log(user_name, user_contact, sport, user_peak)
            st.success(f"✅ {user_name}님의 분석 기록이 서버에 저장되었습니다.")
            
            st.markdown(get_precision_report(sport, gender, user_peak))
            
            # 전문가 연결 링크
            st.divider()
            subject = f"[{sport}] {user_name}님 정밀 분석 피드백 요청"
            body = f"사용자: {user_name}\n측정 각도: {user_peak}도"
            mailto_link = f"mailto:youclsrn1@gmail.com?subject={subject}&body={body}"
            st.markdown(f"📩 [전문가 추가 상담하기]({mailto_link})")
