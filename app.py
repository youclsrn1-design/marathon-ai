import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [마스터 데이터베이스] - 마라톤을 필두로 한 전 종목 데이터
SPORT_MASTER_DB = {
    "마라톤 (풀코스/러닝)": {
        "남성": {"기준": "무릎 신전 및 지면 반발력", "범위": (170, 180), "핵심": "피로 누적으로 인해 보폭(Stride)이 짧아지고 있습니다."},
        "여성": {"기준": "무릎 신전 및 골반 안정성", "범위": (168, 178), "핵심": "착지 시 무릎이 과하게 굽어 에너지 손실이 발생합니다."},
        "출처": "World Athletics Endurance Lab",
        "풀이": "마라톤 후반부에는 무릎이 덜 펴지면서 추진력이 급격히 떨어집니다. AI는 착지 직후 반발 각도를 실시간 추적합니다.",
        "해결": "스마트 글래스의 안내에 따라 골반을 더 앞으로 밀어내며 뒷발을 끝까지 밀어주세요."
    },
    "육상 (단거리/경보)": {
        "남성": {"기준": "무릎 거상/신전", "범위": (85, 180), "핵심": "종목 규칙 및 폭발력 기준 미달 구간이 존재합니다."},
        "여성": {"기준": "무릎 거상/신전", "범위": (80, 178), "핵심": "신체 밸런스 대비 탄력 효율이 떨어지고 있습니다."},
        "출처": "IAAF Technical", "풀이": "단거리는 높이, 경보는 펴짐이 생명입니다.", "해결": "종목별 특화 드릴 훈련이 필요합니다."
    },
    "수영 (4대 영법)": {
        "남성": {"기준": "하이 엘보우/캐치 각도", "범위": (90, 110), "핵심": "캐치 단계에서 팔꿈치가 떨어져 추진력을 잃고 있습니다."},
        "여성": {"기준": "하이 엘보우/캐치 각도", "범위": (85, 105), "핵심": "스트로크 가동 범위가 유연성 대비 좁습니다."},
        "출처": "FINA Coaching", "풀이": "물을 잡는 순간의 각도가 영법의 효율을 결정합니다.", "해결": "팔꿈치를 세우는 하이 엘보우 자세에 집중하세요."
    },
    "야구 (투구/타격)": {
        "남성": {"기준": "회전축 및 릴리즈 각도", "범위": (90, 105), "핵심": "팔꿈치 높이가 낮아 어깨 부상 위험이 높습니다."},
        "여성": {"기준": "회전축 및 릴리즈 각도", "범위": (85, 95), "핵심": "릴리즈 포인트가 불안정하여 제구력이 흔들립니다."},
        "출처": "ASMI Database", "풀이": "투구 시 팔꿈치와 어깨의 수평 정렬이 구속의 핵심입니다.", "해결": "팔꿈치를 귀 옆까지 높이는 훈련을 권장합니다."
    },
    "양궁/사격/바이애슬론": {
        "남성": {"기준": "슈팅 라인 직선도", "범위": (175, 185), "핵심": "격발 시 팔꿈치 수평이 미세하게 흔들립니다."},
        "여성": {"기준": "슈팅 라인 직선도", "범위": (174, 182), "핵심": "드로잉 암의 등 근육 텐션이 일정하지 않습니다."},
        "출처": "World Archery", "풀이": "0.1도의 흔들림이 탄착군을 바꿉니다. 상체 정렬을 분석합니다.", "해결": "견갑골을 모아 자세를 단단히 고정하세요."
    }
}

st.set_page_config(page_title="ATHLETES AI - WEARABLE READY", layout="centered")
st.title("🏃‍♂️ ATHLETES AI: 스마트 글래스 연동 정밀 분석")

# 1. 설정 레이아웃
col1, col2 = st.columns(2)
with col1: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
with col2: event = st.selectbox("분석 종목 (마라톤 포함 전 종목)", list(SPORT_MASTER_DB.keys()))

# 2. 분석 메커니즘 공시
db_info = SPORT_MASTER_DB[event]
gender_data = db_info[gender]
with st.expander(f"👓 AR 글래스 투사 데이터 기준 ({event})", expanded=True):
    st.write(f"✅ **표준 범위:** {gender_data['범위']}° (근거: {db_info['출처']})")
    st.write(f"✅ **실시간 모니터링:** {gender_data['기준']}")

uploaded_file = st.file_uploader("영상을 업로드하세요. AI가 웨어러블 전송 데이터를 시뮬레이션합니다.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # [수정 완료] 오타 수정: CAP_PROP_FRAME_WIDTH (COMM_PROP 에러 해결)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frame_window = st.image([])
    status_text = st.empty()
    data_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark
            
            # 종목별 스마트 트래킹 (상체 vs 하체)
            if any(x in event for x in ["야구", "수영", "양궁"]):
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            else: # 마라톤 및 육상
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            curr_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(curr_angle)
            
            # 영상 위에 AR 데이터 오버레이 표시
            cv2.putText(image, f"LIVE: {curr_angle}deg", (50, 100), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 3)

        frame_window.image(image, channels="RGB")
        status_text.text(f"🏃‍♂️ 마라톤 데이터 트래킹 중... 현재 각도: {curr_angle if data_list else 0}°")

    cap.release()
    st.write("---")
    
    # 3. 3단계 정밀 리포트
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]
    
    st.subheader(f"📊 {gender} {event} 분석 리포트 (Wearable Summary)")
    c1, c2 = st.columns(2)
    c1.metric("내 데이터 평균", f"{user_avg}°")
    c2.metric("전문가 권장 범위", f"{min_s}° ~ {max_s}°")

    st.markdown("#### 🎯 핵심 요약 (AR 브리핑)")
    if min_s <= user_avg <= max_s:
        st.success("에너지 효율이 매우 높습니다. 현재 페이스와 자세를 유지하세요!")
    else:
        st.warning(gender_data["핵심"])
        
    with st.expander("🔍 역학적 분석 (상세 원리)", expanded=True):
        st.write(db_info["풀이"])
    
    st.markdown("#### 🚀 실시간 개선 가이드")
    st.info(db_info["해결"])
    st.balloons()
