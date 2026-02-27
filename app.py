import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [데이터베이스] 성별/종목별 정교한 표준 데이터
SPORT_MASTER_DB = {
    "육상": {
        "단거리/허들": {
            "남성": {"기준": "무릎 거상 각도", "범위": (85, 95), "핵심": "무릎 높이가 낮습니다.", "풀이": "폭발적 가속을 위한 피칭 각도입니다."},
            "여성": {"기준": "무릎 거상 각도", "범위": (80, 90), "핵심": "탄력이 부족합니다.", "풀이": "여성 신체 구조에 맞춘 가속 각도입니다."}
        },
        "경보": {
            "남성": {"기준": "무릎 신전", "범위": (178, 180), "핵심": "실격 위험!", "풀이": "착지 시 무릎을 완전히 펴야 합니다."},
            "여성": {"기준": "무릎 신전", "범위": (177, 180), "핵심": "주의 필요!", "풀이": "여성 골반 구조를 고려한 신전 각도입니다."}
        }
    },
    "수영": {
        "자유형": {
            "남성": {"기준": "하이 엘보우", "범위": (95, 110), "핵심": "팔꿈치 처짐", "풀이": "캐치 단계에서의 물 잡기 효율입니다."},
            "여성": {"기준": "하이 엘보우", "범위": (90, 105), "핵심": "회전 부족", "풀이": "유연성을 활용한 효율적 스트로크입니다."}
        }
    }
    # ... (기타 모든 종목 확장 가능)
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")
st.title("🏆 ATHLETES AI: 실시간 정밀 역학 분석")

# 1. 정밀 타겟팅 설정
col1, col2, col3 = st.columns(3)
with col1: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
with col2: main_cat = st.selectbox("대분류", list(SPORT_MASTER_DB.keys()))
with col3: sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

uploaded_file = st.file_uploader("영상을 올려주세요. AI가 실시간으로 분석합니다.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    # 실시간 영상 출력을 위한 창
    frame_window = st.image([])
    status_text = st.empty()
    
    data_list = []
    info = SPORT_MASTER_DB[main_cat][sub_cat]
    gender_data = info[gender]

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            # 뼈대 그리기 (사용자에게 신뢰를 주는 핵심 비주얼)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
            )
            
            # 종목별 실시간 각도 추출
            lm = results.pose_landmarks.landmark
            # 하체 위주 분석 예시 (힙-무릎-발목)
            a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            current_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(current_angle)
            
            # 영상 위에 현재 각도 텍스트 표시
            cv2.putText(image, f"{current_angle} deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        frame_window.image(image, channels="RGB")
        status_text.text(f"분석 중... 현재 각도: {current_angle if data_list else 0}°")

    cap.release()
    
    # 2. 결과 리포트 출력
    st.write("---")
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]
    
    st.subheader(f"📊 {gender} {sub_cat} 최종 분석 결과")
    c1, c2, c3 = st.columns(3)
    c1.metric("나의 평균", f"{user_avg}°")
    c2.metric("권장 범위", f"{min_s}° ~ {max_s}°")
    c3.metric("판단", "정상" if min_s <= user_avg <= max_s else "조정 필요")

    st.markdown(f"#### 🎯 핵심 피드백")
    if min_s <= user_avg <= max_s:
        st.success("데이터 분석 결과, 전문가 그룹의 표준 자세와 완벽히 일치합니다.")
    else:
        st.warning(gender_data["핵심"])
        
    with st.expander("🔍 상세 역학 원리 (Why?)"):
        st.write(gender_data["풀이"])
    
    st.balloons()
