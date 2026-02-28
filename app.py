import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import os

# --- 1. AI 및 시각화 엔진 설정 ---
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
# 정밀 분석을 위해 모델 복잡도를 1로 유지 (서버 성능과 정확도의 최적점)
pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 📐 [정밀 역학] 관절 사잇각 계산 공식
# 관절 $B$를 꼭짓점으로 하는 두 벡터 $\vec{BA}$와 $\vec{BC}$ 사이의 내적을 이용한 각도 산출
# $$\theta = \arccos \left( \frac{\vec{BA} \cdot \vec{BC}}{|\vec{BA}| |\vec{BC}|} \right)$$
def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0: return 0
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return int(angle)

# 엘리트 선수 데이터베이스 (정밀 분석 기준점)
ELITE_DB = {
    "마라톤": {"남성": 174, "여성": 170},
    "경보": {"남성": 179, "여성": 178}
}

# --- 2. 정밀 분석 리포트 생성기 ---
def get_precision_report(sport, gender, user_angle):
    ref = ELITE_DB[sport][gender]
    diff = user_angle - ref
    
    report = f"## 📊 {sport} 정밀 분석 리포트\n\n"
    
    # [데이터 기반 상태 진단]
    if abs(diff) <= 2:
        report += "⭐ **상태:** 최상급(Elite). 엘리트 선수와 일치하는 완벽한 역학 구조를 보입니다.\n\n"
    elif abs(diff) <= 5:
        report += "✅ **상태:** 양호(Good). 안정적인 폼이나 미세한 가동범위 조정이 권장됩니다.\n\n"
    else:
        report += "⚠️ **상태:** 분석 필요(Caution). 효율적인 추진을 위한 자세 교정이 시급합니다.\n\n"

    # [종목별 전문 코칭 피드백]
    if sport == "마라톤":
        report += "### 💡 역학적 피드백\n"
        if user_angle > ref + 3:
            report += "* **현상:** 착지 시 무릎이 과하게 펴지는 '오버스트라이드' 경향이 보입니다.\n"
            report += "* **교정:** 무릎을 미세하게 굽혀 지면 충격을 흡수하고 회전 리듬을 높이세요.\n"
            report += "* **부상 방지:** 슬개골 및 연골판에 가해지는 수직 부하를 줄여야 합니다.\n"
        else:
            report += "* **현상:** 무릎의 굴곡이 깊어 추진 에너지가 지면으로 분산되고 있습니다.\n"
            report += "* **교정:** 지면을 박차고 나갈 때 대퇴부의 탄성을 더 활용해 보세요.\n"
            report += "* **부상 방지:** 대퇴사두근의 과도한 피로 누적을 주의해야 합니다.\n"
    
    else: # 경보 (Racewalking)
        report += "### 💡 규정 및 역학 피드백\n"
        if user_angle < 178:
            report += "* **현상:** 착지 후 지탱하는 다리의 무릎이 굽혀지는 'Bent Knee' 위험이 감지됩니다.\n"
            report += "* **교정:** 규정 준수를 위해 착지 시점부터 수직점까지 무릎을 완벽히 펴야 합니다.\n"
            report += "* **부상 방지:** 무릎을 펴지 못할 경우 햄스트링 근육의 과부하가 발생할 수 있습니다.\n"
        else:
            report += "* **현상:** 규정에 부합하는 우수한 직선 보행을 유지하고 있습니다.\n"
            report += "* **교정:** 현재의 직선성을 유지하며 골반의 회전 가동범위를 극대화하세요.\n"
            report += "* **부상 방지:** 골반 주변 근육의 유연성 확보를 위해 스트레칭을 병행하세요.\n"
            
    return report

# --- 3. UI/UX 레이아웃 ---
st.set_page_config(page_title="ATHLETES AI: Precision Analysis", layout="wide")
st.title("🏃 ATHLETES AI: 마라톤 & 경보 정밀 분석")

with st.sidebar:
    st.header("👤 선수 프로필")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    st.divider()
    st.markdown("### 📞 전문가 심화 분석")
    st.write("전문가 코칭이 필요하시면 아래로 문의하세요.")
    st.write("youclsrn1@gmail.com")

uploaded_file = st.file_uploader("분석할 훈련 영상을 업로드하세요 (MP4, MOV)", type=["mp4", "mov"])

if uploaded_file:
    # 파일 처리 및 분석 로직
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out_path = "precision_analysis.mp4"
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    angles = []
    with st.spinner('AI 가 정밀 역학 분석을 진행 중입니다...'):
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)
            
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                lm = results.pose_landmarks.landmark
                # 무릎 각도 계산용 좌표 (골반-무릎-발목)
                p1 = [lm[23].x * width, lm[23].y * height]
                p2 = [lm[25].x * width, lm[25].y * height]
                p3 = [lm[27].x * width, lm[27].y * height]
                
                angle = calculate_precise_angle(p1, p2, p3)
                angles.append(angle)
                cv2.putText(frame, f"{angle}deg", (int(p2[0]), int(p2[1])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            out.write(frame)
    
    cap.release(); out.release()

    # 결과 대시보드
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🎥 시각화 분석 결과")
        st.video(out_path)
    with col2:
        user_peak = max(angles) if angles else 0
        st.markdown(get_precision_report(sport, gender, user_peak))
        
        # 전문가 상담 연결
        st.divider()
        subject = f"[{sport}] 정밀 분석 데이터 기반 피드백 요청"
        body = f"측정된 최대 각도: {user_peak}도"
        mailto_link = f"mailto:youclsrn1@gmail.com?subject={subject}&body={body}"
        st.markdown(f"📩 [전문가에게 분석 데이터 보내기]({mailto_link})")
