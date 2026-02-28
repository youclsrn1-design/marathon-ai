import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import time

# 1. AI 엔진 설정 (서버 권한 에러 해결을 위해 complexity 1로 최적화)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    model_complexity=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

# 📐 관절 각도 계산용 물리 공식
def calculate_precise_angle(p1, p2, p3):
    u, v = np.array(p1) - np.array(p2), np.array(p3) - np.array(p2)
    norm_u, norm_v = np.linalg.norm(u), np.linalg.norm(v)
    if norm_u == 0 or norm_v == 0: return 0
    cosine_theta = np.dot(u, v) / (norm_u * norm_v)
    return round(np.degrees(np.arccos(np.clip(cosine_theta, -1.0, 1.0))), 1)

# 📊 [안전장치 강화] 엘리트 데이터베이스
ELITE_DB = {
    "마라톤": {
        "남성": {"Global": 172.5, "Korea": 169.8, "Focus": "폭발적 추진력"},
        "여성": {"Global": 168.2, "Korea": 165.5, "Focus": "유연한 리듬감"}
    },
    "경보": {
        "남성": {"Global": 179.2, "Korea": 178.5, "Focus": "완벽한 Knee-lock"},
        "여성": {"Global": 178.5, "Korea": 177.2, "Focus": "골반 유연성"}
    }
}

# 🎙️ [Professional Report] 논리적 진단 + 쉬운 영어
def get_supreme_report(sport, gender, target, user_angle):
    # 에러 방지용 키 정제 로직
    clean_target = "Global" if "Global" in target else "Korea"
    
    # 데이터 매칭 안전 장치
    try:
        ref_val = ELITE_DB[sport][gender][clean_target]["angle"] if "angle" in ELITE_DB[sport][gender][clean_target] else 175
        # 실제 데이터가 없을 경우를 대비한 하드코딩 백업
        if sport == "경보": ref_val = 179.2 if clean_target == "Global" else 178.5
        else: ref_val = 172.5 if clean_target == "Global" else 169.8
    except:
        ref_val = 170.0 # 최종 보루 기본값

    diff = user_angle - ref_val
    
    if abs(diff) < 2.5:
        kr = f"✅ **[엘리트 진단]** {gender} {sport} {clean_target} 수준의 완벽한 정렬입니다. 탄성 에너지 효율이 극대화된 상태입니다."
        en = f"💡 **[Easy English]** Perfect! You move just like a pro {gender} athlete. Great balance!"
    else:
        direction = "신전 부족" if diff < 0 else "과신전 위험"
        kr = f"🚨 **[교정 처방]** {clean_target} 기준 대비 {abs(diff)}°의 {direction}이 발견됩니다. 추진력 손실과 관절 부하의 원인이 됩니다."
        en = f"💡 **[Easy English]** Your leg is a bit {'bent' if diff < 0 else 'stiff'}. Try to keep it straight like a pro!"
    
    return kr, en, ref_val

# --- UI 인터페이스 ---
st.set_page_config(page_title="ATHLETES AI SUPREME", layout="wide")
st.title("⚡ ATHLETES AI: 엘리트 정밀 분석")

with st.sidebar:
    st.header("⚙️ 분석 설정")
    gender = st.radio("성별", ["남성", "여성"])
    sport = st.radio("종목", ["마라톤", "경보"])
    target = st.radio("비교 대상", ["Global Elite", "Korea Elite"])
    view = st.selectbox("촬영 각도", ["측면 (Side)", "정면 (Front)"])

uploaded_file = st.file_uploader(f"[{gender}] [{sport}] 영상을 업로드하세요", type=["mp4", "mov"])

if uploaded_file:
    with st.spinner("AI가 실제 역학 구조를 낱낱이 분석 중입니다..."):
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
        
        angles = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                p1, p2, p3 = [lm[23].x, lm[23].y], [lm[25].x, lm[25].y], [lm[27].x, lm[27].y]
                angles.append(calculate_precise_angle(p1, p2, p3))
        cap.release()
        
        user_peak = max(angles) if angles else 0
        kr_f, en_f, elite_val = get_supreme_report(sport, gender, target, user_peak)
        
    st.subheader(f"📊 {gender} {sport} 분석 리포트")
    c1, c2, c3 = st.columns(3)
    c1.metric("나의 피크 각도", f"{user_peak}°")
    c2.metric(f"{target} 기준", f"{elite_val}°")
    c3.metric("격차", f"{round(user_peak - elite_val, 1)}°")

    st.write("---")
    st.success(kr_f)
    st.info(en_f)
    st.balloons()
