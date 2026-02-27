import streamlit as st  # 소문자로 수정 완료
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [전 종목 마스터 데이터베이스] - 성별/세부종목별 정밀 데이터
# 주의: 아래 키 이름(예: "육상")은 selectbox 메뉴와 정확히 일치해야 합니다.
SPORT_MASTER_DB = {
    "육상 (마라톤/단거리)": {
        "마라톤 (지구력)": {
            "남성": {"기준": "무릎 신전 각도", "범위": (170, 180), "핵심": "후반부 피로로 인해 추진력이 감소 중입니다."},
            "여성": {"기준": "무릎 신전 각도", "범위": (168, 178), "핵심": "착지 시 무릎 굽힘이 커져 관절 부하가 증가합니다."},
            "출처": "World Athletics", "풀이": "장거리 러닝 시 무릎이 펴지는 각도는 에너지 효율과 직결됩니다.", "해결": "상체를 세우고 골반을 앞으로 밀어 추진력을 확보하세요."
        },
        "단거리/허들": {
            "남성": {"기준": "무릎 거상 각도", "범위": (85, 95), "핵심": "폭발적 가속을 위한 무릎 높이가 낮습니다."},
            "여성": {"기준": "무릎 거상 각도", "범위": (80, 90), "핵심": "탄력적인 피칭을 위한 무릎 높이가 부족합니다."},
            "출처": "IAAF Technical", "풀이": "단거리는 무릎이 골반 높이까지 올라와야 파워가 실립니다.", "해결": "고관절 굴곡근 강화 훈련을 추천합니다."
        }
    },
    "구기 종목 (축구/농구)": {
        "축구 (슈팅/킥)": {
            "남성": {"기준": "임팩트 상체 각도", "범위": (145, 160), "핵심": "상체가 뒤로 넘어가 슛이 높게 뜹니다."},
            "여성": {"기준": "임팩트 상체 각도", "범위": (140, 155), "핵심": "디딤발 안정성이 부족하여 정확도가 떨어집니다."},
            "출처": "KFA Report", "풀이": "임팩트 시 상체를 숙여야 낮고 강한 슈팅이 가능합니다.", "해결": "디딤발을 공 옆에 고정하고 상체 중심을 낮추세요."
        },
        "농구 (점프슛)": {
            "남성": {"기준": "릴리즈 팔꿈치 각도", "범위": (85, 95), "핵심": "팔꿈치가 벌어져 슛의 직진성이 떨어집니다."},
            "여성": {"기준": "릴리즈 팔꿈치 각도", "범위": (80, 90), "핵심": "타점이 낮아 수비의 방해를 받기 쉽습니다."},
            "출처": "NBA Analysis", "풀이": "팔꿈치가 수직 일직선을 이뤄야 일정한 궤적이 유지됩니다.", "해결": "팔꿈치를 안으로 모으고 손목 스냅을 활용하세요."
        }
    },
    "라켓 스포츠 (테니스/탁구)": {
        "테니스 (포핸드)": {
            "남성": {"기준": "임팩트 팔 확장", "범위": (150, 170), "핵심": "타점이 너무 가까워 파워 전달이 안 됩니다."},
            "여성": {"기준": "임팩트 팔 확장", "범위": (145, 165), "핵심": "스윙 궤적이 좁아 회전력이 부족합니다."},
            "출처": "ITF Coaching", "풀이": "임팩트 시 팔이 적절히 뻗어져야 강한 구질이 형성됩니다.", "해결": "공과의 거리를 두고 앞으로 던지듯 스윙하세요."
        },
        "탁구 (드라이브)": {
            "남성": {"기준": "무릎 중심 이동", "범위": (120, 140), "핵심": "하체 중심이 높아 회전력이 부족합니다."},
            "여성": {"기준": "무릎 중심 이동", "범위": (115, 135), "핵심": "임팩트 시 상하체 밸런스가 무너지고 있습니다."},
            "출처": "ITTF Manual", "풀이": "하체에서 상체로 힘을 전달하려면 무릎을 낮춰야 합니다.", "해결": "기마 자세를 유지하며 골반 회전과 함께 스윙하세요."
        }
    },
    "수영 (4대 영법)": {
        "자유형/배영": {
            "남성": {"기준": "하이 엘보우 각도", "범위": (95, 110), "핵심": "캐치 단계에서 팔꿈치가 떨어져 추진력이 상실됩니다."},
            "여성": {"기준": "하이 엘보우 각도", "범위": (90, 105), "핵심": "스트로크 가동 범위가 유연성 대비 좁습니다."},
            "출처": "FINA Standards", "풀이": "팔꿈치를 높게 유지해야 물을 뒤로 밀어내는 힘이 생깁니다.", "해결": "손목보다 팔꿈치를 높게 유지하며 물을 미세요."
        }
    }
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")
st.title("🏆 ATHLETES AI: 전 종목 맞춤형 정밀 분석")

# 1. 입력 설정
gender = st.radio("성별", ["남성", "여성"], horizontal=True)
main_cat = st.selectbox("대분류", list(SPORT_MASTER_DB.keys()))
sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

# 2. 분석 기준 사전 공개
db_info = SPORT_MASTER_DB[main_cat][sub_cat]
gender_data = db_info[gender]
with st.expander(f"🔬 {gender} {sub_cat} 분석 기준 확인", expanded=True):
    st.write(f"✅ **표준 범위:** {gender_data['범위']}° (근거: {db_info['출처']})")
    st.write(f"✅ **핵심 모니터링:** {gender_data['기준']}")

uploaded_file = st.file_uploader("영상을 업로드하세요.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # 에러 수정 완료: CAP_PROP_FRAME_WIDTH
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
            
            # 상체 중심 vs 하체 중심 종목 좌표 분기
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
            
            cv2.putText(image, f"ANGLE: {curr_angle}deg", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        frame_window.image(image, channels="RGB")
        status_text.text(f"분석 중... 현재 데이터: {curr_angle if data_list else 0}°")

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
    st.info(db_info.get("해결", "자세 교정 훈련을 통해 효율을 높이세요."))
    st.balloons()

