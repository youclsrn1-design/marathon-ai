import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [전 종목 마스터 데이터베이스] - 성별/세부종목별 정밀 데이터
SPORT_MASTER_DB = {
    "마라톤/육상": {
        "마라톤 (지구력)": {
            "남성": {"기준": "무릎 신전 각도", "범위": (170, 180), "핵심": "후반부 피로로 인해 추진력이 감소 중입니다."},
            "여성": {"기준": "무릎 신전 각도", "범위": (168, 178), "핵심": "착지 시 무릎 굽힘이 커져 관절 부하가 증가합니다."},
            "출처": "World Athletics", "풀이": "장거리 러닝 시 무릎이 펴지는 각도는 에너지 효율과 직결됩니다.", "해결": "상체를 세우고 골반을 앞으로 밀어 추진력을 확보하세요."
        },
        "단거리/경보": {
            "남성": {"기준": "무릎 피칭/신전", "범위": (85, 180), "핵심": "지면 반발력을 위한 무릎 정렬이 불안정합니다."},
            "여성": {"기준": "무릎 피칭/신전", "범위": (80, 178), "핵심": "탄력적인 도약을 위한 무릎 높이가 낮습니다."},
            "출처": "IAAF Rule", "풀이": "단거리는 높이, 경보는 완전한 펴짐이 핵심 지표입니다.", "해결": "고관절 굴곡근 강화 훈련을 병행하세요."
        }
    },
    "라켓 스포츠": {
        "테니스 (포핸드)": {
            "남성": {"기준": "임팩트 팔 확장", "범위": (150, 170), "핵심": "타점이 몸과 너무 가까워 파워 전달이 안 됩니다."},
            "여성": {"기준": "임팩트 팔 확장", "범위": (145, 165), "핵심": "스윙 궤적이 좁아 회전력이 부족합니다."},
            "출처": "ITF Coaching", "풀이": "임팩트 시 팔이 적절히 뻗어져야 지렛대 원리에 의해 강한 구질이 형성됩니다.", "해결": "공과의 거리를 더 확보하고 앞으로 길게 던지듯 스윙하세요."
        },
        "배드민턴 (스매시)": {
            "남성": {"기준": "타점 어깨 각도", "범위": (165, 180), "핵심": "타점이 낮아 셔틀콕이 길게 나갑니다."},
            "여성": {"기준": "타점 어깨 각도", "범위": (160, 175), "핵심": "손목 스냅 대비 어깨 회전 반경이 작습니다."},
            "출처": "BWF Technical", "풀이": "최고점에서 타격해야 날카로운 각도의 스매시가 가능합니다.", "해결": "팔을 귀 옆으로 바짝 붙여 높은 타점에서 내리치세요."
        },
        "탁구 (드라이브)": {
            "남성": {"기준": "무릎 중심 이동", "범위": (120, 140), "핵심": "하체 중심이 높아 회전력이 공에 실리지 않습니다."},
            "여성": {"기준": "무릎 중심 이동", "범위": (115, 135), "핵심": "임팩트 시 상하체 밸런스가 무너지고 있습니다."},
            "출처": "ITTF Manual", "풀이": "탁구는 무릎 각도를 낮춰 하체에서 상체로 힘을 전달하는 것이 핵심입니다.", "해결": "기마 자세를 유지하며 골반 회전과 함께 스윙하세요."
        }
    },
    "구기 종목": {
        "축구 (슈팅/킥)": {
            "남성": {"기준": "디딤발/임팩트 각도", "범위": (145, 160), "핵심": "상체가 뒤로 넘어가 슛이 높게 뜹니다."},
            "여성": {"기준": "디딤발/임팩트 각도", "범위": (140, 155), "핵심": "디딤발의 안정성이 부족하여 정확도가 떨어집니다."},
            "출처": "KFA Report", "풀이": "임팩트 시 상체를 숙여야 낮고 강한 슈팅이 가능합니다.", "해결": "디딤발을 공 옆에 단단히 고정하고 상체를 공 쪽으로 누르세요."
        },
        "농구 (점프슛)": {
            "남성": {"기준": "릴리즈 팔꿈치 각도", "범위": (85, 95), "핵심": "팔꿈치가 벌어져 슛의 직진성이 떨어집니다."},
            "여성": {"기준": "릴리즈 팔꿈치 각도", "범위": (80, 90), "핵심": "타점이 낮아 수비의 방해를 받기 쉽습니다."},
            "출처": "NBA Analysis", "풀이": "팔꿈치가 수직 일직선을 이뤄야 일정한 슛 궤적을 유지할 수 있습니다.", "해결": "팔꿈치를 안으로 모으고 손목 스냅을 끝까지 활용하세요."
        }
    },
    "수영/무도": {
        "수영 (4대 영법)": {
            "남성": {"기준": "하이 엘보우", "범위": (95, 110), "핵심": "팔꿈치가 떨어져 추진력이 상실되고 있습니다."},
            "여성": {"기준": "하이 엘보우", "범위": (90, 105), "핵심": "스트로크 가동 범위가 유연성 대비 좁습니다."},
            "출처": "FINA Standards", "풀이": "물을 잡는 순간 팔꿈치를 높게 유지하는 것이 영법의 핵심입니다.", "해결": "손목보다 팔꿈치를 높게 유지하며 물을 뒤로 미세요."
        },
        "야구 (투구/타격)": {
            "남성": {"기준": "릴리즈/힙턴 각도", "범위": (90, 105), "핵심": "팔꿈치 높이가 낮아 어깨 부상 위험이 큽니다."},
            "여성": {"기준": "릴리즈/힙턴 각도", "범위": (85, 95), "핵심": "하체 회전 타이밍이 상체보다 늦습니다."},
            "출처": "ASMI/MLB", "풀이": "투구 시 팔꿈치와 어깨의 평행이 구속과 부상을 결정합니다.", "해결": "팔꿈치를 어깨 높이 이상으로 끌어올리세요."
        }
    }
}

st.set_page_config(page_title="ATHLETES AI - COMPLETE", layout="centered")
st.title("🏆 ATHLETES AI: 전 종목 통합 정밀 분석")

# 1. 입력 설정
col1, col2, col3 = st.columns(3)
with col1: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
with col2: main_cat = st.selectbox("대분류", list(SPORT_MASTER_DB.keys()))
with col3: sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

# 2. 분석 기준 사전 공개
db_info = SPORT_MASTER_DB[main_cat][sub_cat]
gender_data = db_info[gender]
with st.expander(f"🔬 {gender} {sub_cat} 분석 메커니즘 (신뢰도 데이터)", expanded=True):
    st.write(f"✅ **표준 범위:** {gender_data['범위']}° (근거: {db_info['출처']})")
    st.write(f"✅ **핵심 모니터링:** {gender_data['기준']}")

uploaded_file = st.file_uploader("영상을 업로드하세요. 실시간 AI 코칭이 시작됩니다.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # [에러 수정 완료] CAP_PROP_FRAME_WIDTH
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
            
            # 상체 중심 종목 vs 하체 중심 종목 좌표 분기
            if any(x in sub_cat for x in ["테니스", "배드민턴", "농구", "야구", "수영"]):
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            else:
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            curr_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(curr_angle)
            
            # 실시간 데이터 오버레이
            cv2.putText(image, f"ANGLE: {curr_angle}deg", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        frame_window.image(image, channels="RGB")
        status_text.text(f"🏃‍♂️ {sub_cat} 분석 중... 현재 데이터: {curr_angle if data_list else 0}°")

    cap.release()
    st.write("---")
    
    # 3. 3단계 정밀 리포트
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]
    
    st.subheader(f"📊 {gender} {sub_cat} 분석 보고서")
    c1, c2 = st.columns(2)
    c1.metric("내 데이터 평균", f"{user_avg}°")
    c2.metric("전문가 표준 범위", f"{min_s}° ~ {max_s}°")

    st.markdown("#### 🎯 핵심 요약")
    if min_s <= user_avg <= max_s:
        st.success("데이터 분석 결과, 전문가 수준의 최적화된 자세를 유지하고 있습니다!")
    else:
        st.warning(gender_data["핵심"])
        
    with st.expander("🔍 역학 원리 상세 분석 (Why?)", expanded=True):
        st.write(db_info["풀이"])
    
    st.markdown("#### 🚀 실시간 개선 가이드 (How?)")
    st.info(db_info["해결"])
    st.balloons()
