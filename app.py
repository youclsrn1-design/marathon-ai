import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 및 시각화 도구 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [전 종목 마스터 데이터베이스] 성별/영법/종목별 정밀 기준
SPORT_MASTER_DB = {
    "육상": {
        "단거리/허들": {
            "남성": {"범위": (85, 95), "핵심": "무릎 피칭 높이가 낮습니다.", "풀이": "남성 엘리트 스프린터는 가속 시 무릎이 골반 높이까지 올라와야 파워가 실립니다."},
            "여성": {"범위": (80, 90), "핵심": "지면 반발력을 충분히 활용하지 못하고 있습니다.", "풀이": "여성 신체 구조상 골반의 탄력을 이용한 무릎 거상이 기록 단축의 핵심입니다."},
            "출처": "World Athletics Performance Lab", "해결책": "고관절 굴곡근 강화 훈련과 높은 무릎 들기 드릴을 병행하세요."
        },
        "경보": {
            "남성": {"범위": (178, 180), "핵심": "착지 순간 무릎이 미세하게 굽어 반칙 위험이 큽니다.", "풀이": "IAAF 230.1조에 의거, 착지 시 무릎은 완전히 펴져야 합니다."},
            "여성": {"범위": (177, 180), "핵심": "골반 회전 시 무릎 고정이 흔들립니다.", "풀이": "여성 골반의 큰 가동 범위를 제어하기 위한 무릎 신전 능력을 분석합니다."},
            "출처": "IAAF Technical Rule", "해결책": "착지 직전 대퇴사두근에 힘을 주어 관절을 완전히 잠그는 연습을 하세요."
        }
    },
    "수영": {
        "자유형/배영": {
            "남성": {"범위": (95, 110), "핵심": "캐치 단계에서 팔꿈치가 떨어져 물을 잡지 못합니다.", "풀이": "하이 엘보우 각도가 무너지면 추진력이 아닌 저항만 발생합니다."},
            "여성": {"범위": (90, 105), "핵심": "스트로크 아크가 신체 비율 대비 짧습니다.", "풀이": "여성의 유연성을 활용하여 물을 더 길게 밀어내는 궤적이 필요합니다."},
            "출처": "FINA Coaching Manual", "해결책": "물을 잡는 순간 팔꿈치를 세워 '높은 벽'을 만든다는 느낌으로 당기세요."
        },
        "평영/접영": {
            "남성": {"범위": (45, 60), "핵심": "킥의 폭이 너무 넓어 강력한 저항을 유발합니다.", "풀이": "평영 킥은 뒤로 밀어내는 힘이 핵심이며, 옆으로 벌어지는 각도는 저항일 뿐입니다."},
            "여성": {"범위": (40, 55), "핵심": "킥 마무리의 탄력이 부족하여 글라이딩 속도가 떨어집니다.", "풀이": "유연한 무릎 굴곡을 추진력으로 바꾸는 마지막 스냅이 필요합니다."},
            "출처": "Swimming Biomechanics", "해결책": "무릎 사이 간격을 어깨너비로 유지하며 발바닥으로 물을 끝까지 밀어내세요."
        }
    },
    "야구/양궁/사격": {
        "야구 (투구)": {
            "남성": {"범위": (90, 105), "핵심": "팔꿈치가 어깨 선보다 낮아 부상 위험과 구속 저하가 우려됩니다.", "풀이": "어깨 회전축과 팔꿈치의 수평 정렬을 분석하여 효율적인 릴리즈를 체크합니다."},
            "여성": {"범위": (85, 95), "핵심": "신체 밸런스 대비 팔꿈치 거상 높이가 일정하지 않습니다.", "풀이": "여성 투수는 어깨 유연성을 활용한 일정한 릴리즈 포인트 유지가 생명입니다."},
            "출처": "ASMI Database", "해결책": "쉐도우 피칭을 통해 팔꿈치 높이를 귀 옆까지 끌어올리는 연습을 하세요."
        },
        "양궁/사격": {
            "남성": {"범위": (175, 182), "핵심": "격발/슈팅 시 상체 라인의 미세한 흔들림이 감지됩니다.", "풀이": "조준 시 팔의 수평 직선도가 무너지면 원거리 명중률이 급격히 하락합니다."},
            "여성": {"범위": (174, 180), "핵심": "화살을 당기는 팔의 팔꿈치가 정점을 지나쳐 흔들립니다.", "풀이": "신체 정렬을 통해 등 근육의 텐션을 일정하게 유지하는지 분석합니다."},
            "출처": "World Archery Standards", "해결책": "견갑골을 모으는 힘으로 활을 유지하고 팔꿈치 수평을 고정하세요."
        }
    }
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")
st.title("🏆 ATHLETES AI: 실시간 전 종목 정밀 코칭")

# 1. 사용자 맞춤 설정
col1, col2, col3 = st.columns(3)
with col1: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
with col2: main_cat = st.selectbox("대분류", list(SPORT_MASTER_DB.keys()))
with col3: sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

# 2. 분석 기준 사전 공개 (신뢰도 확보)
info = SPORT_MASTER_DB[main_cat][sub_cat]
gender_data = info[gender]
with st.expander(f"🔍 {gender} {sub_cat} 분석 메커니즘 확인", expanded=True):
    st.write(f"✅ **표준 범위:** {gender_data['범위']}° (근거: {info['출처']})")
    st.write(f"✅ **분석 포인트:** {gender_data['기준']} 추적")

uploaded_file = st.file_uploader("분석할 영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # [수정 완료] 오타 수정: COMM_PROP -> CAP_PROP
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
            # 실시간 뼈대 시각화
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            lm = results.pose_landmarks.landmark
            # 종목별 좌표 자동 선택 (상체 vs 하체)
            if main_cat in ["수영", "야구/양궁/사격"]:
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            else:
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            current_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(current_angle)
            
            cv2.putText(image, f"{current_angle} deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        frame_window.image(image, channels="RGB")
        status_text.text(f"분석 중... 현재 각도: {current_angle if data_list else 0}°")

    cap.release()
    st.write("---")
    
    # 3. 정밀 3단계 리포트 출력
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]
    
    st.subheader(f"📊 {gender} {sub_cat} 최종 분석 결과")
    c1, c2 = st.columns(2)
    c1.metric("내 측정값 평균", f"{user_avg}°")
    c2.metric(f"권장 표준 범위", f"{min_s}° ~ {max_s}°")

    st.markdown("### 🎯 핵심 요약")
    if min_s <= user_avg <= max_s:
        st.success(f"동작이 매우 정확합니다! {gender} 프로 선수들의 표준 궤적을 유지하고 있습니다.")
    else:
        st.warning(gender_data["핵심"])
        
    with st.expander("🔍 상세 역학 원리 (Why?)", expanded=True):
        st.write(gender_data["풀이"])
    
    st.markdown("### 🚀 맞춤 해결책 (How?)")
    st.info(gender_data["해결책"])
    st.balloons()
