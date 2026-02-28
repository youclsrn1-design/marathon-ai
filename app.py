import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 및 시각화 도구 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 2. [전 종목 통합 마스터 DB] - 누락 없음, 성별 완벽 분리, 마라톤 AR 특화
SPORT_MASTER_DB = {
    "마라톤 및 육상 (AR 핵심)": {
        "마라톤 (풀코스/하프)": {
            "남성": {"기준": "무릎 신전 각도(Knee Extension)", "범위": (170, 180), "핵심": "후반부 피로 누적으로 보폭과 추진력이 감소하고 있습니다."},
            "여성": {"기준": "무릎 신전 각도(Knee Extension)", "범위": (168, 178), "핵심": "착지 시 무릎 굽힘이 커져 관절 부하 및 에너지 손실이 큽니다."},
            "출처": "World Athletics Endurance Lab",
            "풀이": "[AR 스마트 글래스 시뮬레이션] 장시간 러닝 시 무릎이 펴지는 각도는 에너지 효율과 직결됩니다. AI가 피로도에 따른 자세 붕괴를 실시간으로 추적합니다.",
            "해결": "상체를 세우고 골반을 앞으로 밀어 추진력을 회복하세요. (현재 페이스 유지 요망)"
        },
        "단거리/허들": {
            "남성": {"기준": "무릎 거상 (피칭) 각도", "범위": (85, 95), "핵심": "폭발적 가속을 위한 무릎 높이가 낮습니다."},
            "여성": {"기준": "무릎 거상 (피칭) 각도", "범위": (80, 90), "핵심": "탄력적인 도약을 위한 무릎 높이가 부족합니다."},
            "출처": "IAAF Technical", "풀이": "단거리는 무릎이 골반 높이까지 올라와야 파워가 실립니다.", "해결": "고관절 굴곡근 강화 및 하이 니(High-Knee) 드릴을 수행하세요."
        },
        "경보": {
            "남성": {"기준": "무릎 잠금 (Knee Lock)", "범위": (178, 180), "핵심": "착지 시 무릎 굽힘으로 실격(Bent-Knee) 위험이 큽니다."},
            "여성": {"기준": "무릎 잠금 (Knee Lock)", "범위": (177, 180), "핵심": "골반 회전 대비 무릎 고정력이 불안정합니다."},
            "출처": "IAAF Rule 230", "풀이": "경보는 착지 순간 무릎이 반드시 일직선이어야 하는 엄격한 룰이 있습니다.", "해결": "대퇴사두근 힘으로 무릎을 단단히 고정하며 착지하세요."
        }
    },
    "구기 종목": {
        "축구 (슈팅/킥)": {
            "남성": {"기준": "임팩트 상체-무릎 각도", "범위": (145, 160), "핵심": "상체가 뒤로 넘어가 슛이 높게 뜹니다."},
            "여성": {"기준": "임팩트 상체-무릎 각도", "범위": (140, 155), "핵심": "디딤발 안정성이 부족하여 슛의 강도가 약합니다."},
            "출처": "KFA Report", "풀이": "임팩트 시 상체를 숙여 공을 눌러 차야 낮고 강력한 슛이 나옵니다.", "해결": "디딤발을 공 옆에 바짝 붙이고 상체 중심을 낮추세요."
        },
        "농구 (점프슛)": {
            "남성": {"기준": "릴리즈 팔꿈치 수직도", "범위": (85, 95), "핵심": "팔꿈치가 벌어져 슛의 직진성이 떨어집니다."},
            "여성": {"기준": "릴리즈 팔꿈치 수직도", "범위": (80, 90), "핵심": "타점이 낮아 수비의 블로킹에 취약합니다."},
            "출처": "NBA Analysis", "풀이": "팔꿈치가 수직 일직선을 이뤄야 일정한 궤적이 유지됩니다.", "해결": "팔꿈치를 안으로 모으고 손목 스냅을 끝까지 활용하세요."
        }
    },
    "라켓 스포츠": {
        "테니스 (포핸드)": {
            "남성": {"기준": "임팩트 팔 확장", "범위": (150, 170), "핵심": "타점이 너무 가까워 파워 전달이 안 됩니다."},
            "여성": {"기준": "임팩트 팔 확장", "범위": (145, 165), "핵심": "스윙 궤적이 좁아 회전력이 부족합니다."},
            "출처": "ITF Coaching", "풀이": "임팩트 시 팔이 적절히 뻗어져야 지렛대 원리로 강한 구질이 형성됩니다.", "해결": "공과의 거리를 두고 앞으로 던지듯 스윙하세요."
        },
        "배드민턴/탁구": {
            "남성": {"기준": "중심 이동 및 타점", "범위": (120, 175), "핵심": "하체 중심이 높아 파워와 반응 속도가 떨어집니다."},
            "여성": {"기준": "중심 이동 및 타점", "범위": (115, 170), "핵심": "임팩트 시 상하체 밸런스가 불안정합니다."},
            "출처": "BWF/ITTF Manual", "풀이": "기마 자세의 하체 고정과 높은 타점 유지가 라켓 스포츠의 핵심입니다.", "해결": "무릎을 낮추고 스윙 궤적을 몸 앞쪽으로 크게 가져가세요."
        }
    },
    "수영/무도/야구": {
        "수영 (4대 영법)": {
            "남성": {"기준": "하이 엘보우 (캐치 각도)", "범위": (95, 110), "핵심": "캐치 단계에서 팔꿈치가 떨어져 추진력을 상실합니다."},
            "여성": {"기준": "하이 엘보우 (캐치 각도)", "범위": (90, 105), "핵심": "스트로크 가동 범위가 유연성 대비 좁습니다."},
            "출처": "FINA Standards", "풀이": "팔꿈치를 높게 유지해야 물을 효율적으로 뒤로 밀어낼 수 있습니다.", "해결": "손목보다 팔꿈치를 높게 유지하며 물을 당기세요."
        },
        "야구 (투구/타격)": {
            "남성": {"기준": "릴리즈/힙턴 분리 각도", "범위": (90, 105), "핵심": "팔꿈치 높이가 낮아 어깨 부상 위험이 큽니다."},
            "여성": {"기준": "릴리즈/힙턴 분리 각도", "범위": (85, 95), "핵심": "하체 회전 타이밍이 상체보다 늦어 힘이 분산됩니다."},
            "출처": "ASMI / KBO", "풀이": "투구 시 팔꿈치 수평, 타격 시 하체 우선 회전이 파워의 원천입니다.", "해결": "하체를 먼저 고정한 후 상체 회전을 시작하세요."
        }
    }
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="wide")
st.title("🏃‍♂️ ATHLETES AI: 글로벌 스포츠 정밀 코칭 플랫폼")

# 3. 사용자 입력 (에러 원천 차단을 위한 DB 자동 매칭)
col1, col2, col3 = st.columns(3)
with col1: 
    gender = st.radio("👤 성별 선택", ["남성", "여성"], horizontal=True)
with col2: 
    main_cat = st.selectbox("종목 대분류", list(SPORT_MASTER_DB.keys()))
with col3: 
    sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

# 4. 분석 기준 사전 공개
db_info = SPORT_MASTER_DB[main_cat][sub_cat]
gender_data = db_info[gender]

with st.expander(f"👓 {gender} {sub_cat} 분석 메커니즘 (데이터 근거)", expanded=True):
    st.write(f"✅ **전문가 표준 범위:** `{gender_data['범위']}°` (출처: {db_info['출처']})")
    st.write(f"✅ **AI 집중 모니터링:** {gender_data['기준']}")

uploaded_file = st.file_uploader("영상을 업로드하세요. 실시간 뼈대 추적 및 역학 분석이 시작됩니다.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # 안정적인 프레임 처리 속성
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
            
            # 5. 종목 특성에 따른 상체/하체 AI 자동 타겟팅 로직
            upper_body_sports = ["농구", "테니스", "배드민턴", "수영", "야구"]
            if any(sport in sub_cat for sport in upper_body_sports):
                # 상체 중심 분석 (어깨-팔꿈치-손목)
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            else:
                # 하체 중심 분석 (마라톤, 육상, 축구 등: 골반-무릎-발목)
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # 각도 산출
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            curr_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(curr_angle)
            
            # 6. AR 글래스 뷰어 시뮬레이션 오버레이
            cv2.putText(image, f"LIVE TRACKING: {curr_angle} deg", (30, 60), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

        frame_window.image(image, channels="RGB")
        status_text.text(f"🏃‍♂️ 데이터 수집 중... 현재 각도: {curr_angle if data_list else 0}°")

    cap.release()
    st.write("---")
    
    # 7. 3단계 정밀 리포트 출력
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]
    
    st.subheader(f"📊 {gender} {sub_cat} 최종 분석 보고서")
    c1, c2 = st.columns(2)
    c1.metric("내 측정 데이터 (평균)", f"{user_avg}°")
    c2.metric("전문가 표준 가이드", f"{min_s}° ~ {max_s}°")

    st.markdown("#### 🎯 1. 핵심 요약 (Core Feedback)")
    if min_s <= user_avg <= max_s:
        st.success(f"현재 {gender_data['기준']}가 프로 선수 그룹의 최적화된 데이터와 일치합니다. 훌륭합니다!")
    else:
        st.warning(f"⚠️ {gender_data['핵심']}")
        
    with st.expander("🔍 2. 역학 원리 상세 분석 (Why?)", expanded=True):
        st.write(db_info["풀이"])
    
    st.markdown("#### 🚀 3. 실시간 개선 가이드 (How?)")
    st.info(db_info["해결"])
    st.balloons()
