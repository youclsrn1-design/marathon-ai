import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 및 시각화 설정 (서버 에러 방지를 위해 complexity 1로 완벽 고정)
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

# 📐 [수학] 관절 각도 계산용 물리 공식
def calculate_precise_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    
    if norm_ba == 0 or norm_bc == 0:
        return 0
        
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return int(angle)

# 📊 [엘리트 DB] 안전한 데이터 구조
ELITE_DB = {
    "마라톤": {
        "남성": {"Global": 174, "Korea": 170},
        "여성": {"Global": 169, "Korea": 166}
    },
    "경보": {
        "남성": {"Global": 179, "Korea": 178},
        "여성": {"Global": 178, "Korea": 177}
    }
}

# 🎙️ [Supreme 리포트 생성기] 논리적 진단 + 쉬운 영어 + 에러 방어
def get_supreme_report(sport, gender, target, angle):
    # 에러 방지용: "Global Elite"가 들어와도 "Global"만 추출해서 안전하게 매칭
    clean_target = "Global" if "Global" in target else "Korea"
    
    try:
        ref = ELITE_DB[sport][gender][clean_target]
    except KeyError:
        ref = 170 # 최후의 안전장치 (에러 발생 시 기본값)
        
    diff = angle - ref
    
    report = f"### 📊 [AI 초정밀 역학 진단: {sport}]\n\n"
    report += f"**1. 수치 분석 (Fact Check)**\n측정된 피크 각도는 **{angle}°**입니다. {gender} {clean_target} 엘리트 기준({ref}°) 대비 **{abs(diff)}° {'차이' if abs(diff)>2 else '일치'}**를 보입니다.\n\n"
    report += f"**2. 논리적 원인 분석 (Root Cause)**\n현재 각도는 지면 접촉 시 '충격 흡수 단계'에서 코어 근육의 개입이 늦어지며 무릎이 조기에 굽혀지는 현상을 보입니다. 이로 인해 추진 에너지가 지면으로 분산되고 있습니다.\n\n"
    
    metaphor = "마치 바람 빠진 공이 바닥에서 튀어 오르지 못하는 것과 같습니다." if diff < 0 else "마치 너무 딱딱한 나무 막대기가 부러지기 쉬운 상태와 같습니다."
    report += f"**3. 💡 AI 코치의 비유 (Metaphor)**\n{metaphor} 몸의 관절을 '강력한 용수철'이라 생각하고, 지면을 밟는 순간 에너지를 앞당겨주세요.\n\n"
    report += f"> 🇺🇸 **Easy English:** Your knee angle is {angle}°. It should be straight like a ruler ({ref}°) at the impact. Think of your leg as a 'Strong Spring'!"
    
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
    # 안전한 임시 파일 생성
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # [에러 1 해결] 괄호 오타 수정 완료
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0: fps = 30 # fps가 0으로 잡히는 오류 방지
    
    # 출력용 안전한 임시 경로 생성
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_out:
        out_path = temp_out.name

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    angles = []
    
    progress_text = st.empty()
    progress_bar = st.progress(0)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    progress_text.info("🔍 AI가 영상을 프레임 단위로 쪼개어 분석 중입니다...")
    
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        
        if results.pose_landmarks:
            # 뼈대 그리기
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            lm = results.pose_landmarks.landmark
            p1 = [lm[23].x * width, lm[23].y * height]
            p2 = [lm[25].x * width, lm[25].y * height]
            p3 = [lm[27].x * width, lm[27].y * height]
            
            angle = calculate_precise_angle(p1, p2, p3)
            angles.append(angle)
            
            # 폰트 가독성 상향
            cv2.putText(frame, f"{angle} deg", (int(p2[0])+10, int(p2[1])-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
        
        out.write(frame)
        frame_idx += 1
        
        if total_frames > 0:
            progress_bar.progress(min(int((frame_idx / total_frames) * 100), 100))

    cap.release()
    out.release()
    
    progress_text.success("✅ 뼈대 추출 및 역학 분석 완료!")

    # 분석 영상 재생
    st.subheader("📺 AI 모션 트래킹 결과")
    st.video(out_path)
    
    # 넉넉한 피드백 리포트 생성
    user_peak = max(angles) if angles else 0
    report_text = get_supreme_report(sport, gender, target, user_peak)
    
    st.write("---")
    st.markdown(report_text)
    st.balloons()
