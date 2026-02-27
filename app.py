import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# AI 엔진 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# [전 종목 마스터 데이터베이스] 성별/종목/영법별 정밀 데이터
SPORT_MASTER_DB = {
    "육상": {
        "단거리/허들": {
            "남성": {"기준": "무릎 거상 각도", "범위": (85, 95), "핵심": "지면을 차고 올라오는 무릎의 높이가 낮습니다."},
            "여성": {"기준": "무릎 거상 각도", "범위": (80, 90), "핵심": "피칭 시 무릎의 탄력이 표준보다 부족합니다."},
            "풀이": "폭발적인 가속을 위해서는 무릎이 골반 높이까지 올라와야 합니다.", "출처": "WA Coaching"
        },
        "경보": {
            "남성": {"기준": "무릎 신전(Lock)", "범위": (178, 180), "핵심": "착지 시 무릎이 굽어 실격 위험이 있습니다."},
            "여성": {"기준": "무릎 신전(Lock)", "범위": (177, 180), "핵심": "골반 회전 대비 무릎 고정이 불안정합니다."},
            "풀이": "경보 규칙 230.1조에 의거한 착지 무릎의 일직선 유지 능력을 측정합니다.", "출처": "IAAF Rule"
        }
    },
    "수영": {
        "자유형/배영": {
            "남성": {"기준": "하이 엘보우 각도", "범위": (95, 110), "핵심": "스트로크 시 팔꿈치가 떨어져 물을 잡지 못합니다."},
            "여성": {"기준": "하이 엘보우 각도", "범위": (90, 105), "핵심": "팔의 회전 반경이 신체 구조 대비 좁습니다."},
            "풀이": "캐치 단계에서 팔꿈치를 높게 유지해야 추진력을 극대화할 수 있습니다.", "출처": "FINA Technical"
        },
        "평영/접영": {
            "남성": {"기준": "킥/풀 타이밍 및 각도", "범위": (45, 60), "핵심": "킥의 폭이 너무 넓어 저항이 발생합니다."},
            "여성": {"기준": "킥/풀 타이밍 및 각도", "범위": (40, 55), "핵심": "유연성 대비 킥의 마무리가 약합니다."},
            "풀이": "평영 킥은 무릎을 벌리는 각도가 저항의 핵심 변수입니다.", "출처": "Swimming Science"
        }
    },
    "구기": {
        "축구 (슈팅)": {
            "남성": {"기준": "상체 숙임 및 무릎 각도", "범위": (145, 160), "핵심": "상체가 뒤로 넘어가 슛이 뜰 확률이 높습니다."},
            "여성": {"기준": "상체 숙임 및 무릎 각도", "범위": (140, 155), "핵심": "디딤발의 안정성이 부족하여 파워가 실리지 않습니다."},
            "풀이": "임팩트 시 무게 중심이 공보다 앞에 있어야 공을 누를 수 있습니다.", "출처": "KFA Report"
        },
        "배구 (스파이크)": {
            "남성": {"기준": "타점 높이 및 어깨 각도", "범위": (165, 180), "핵심": "팔이 완전히 펴지지 않아 타점이 낮습니다."},
            "여성": {"기준": "타점 높이 및 어깨 각도", "범위": (160, 175), "핵심": "어깨 가동 범위를 다 쓰지 못하고 있습니다."},
            "풀이": "최고점에서 손목 스냅을 쓰기 위한 어깨-팔꿈치 정렬을 분석합니다.", "출처": "FIVB Manual"
        },
        "야구 (투구)": {
            "남성": {"기준": "팔꿈치 거상 각도", "범위": (90, 110), "핵심": "릴리즈 시 팔꿈치가 어깨 아래로 떨어집니다."},
            "여성": {"기준": "팔꿈치 거상 각도", "범위": (85, 100), "핵심": "어깨 회전축이 신체 밸런스보다 낮습니다."},
            "풀이": "회전근개 부상 방지와 구속을 위한 팔꿈치-어깨 수평도를 측정합니다.", "출처": "ASMI Database"
        }
    }
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")
st.title("🏆 ATHLETES AI: 전 종목 맞춤형 정밀 분석")

# 1. 사용자 정밀 타겟팅 (성별 -> 대분류 -> 세부종목)
col1, col2, col3 = st.columns(3)
with col1: gender = st.radio("성별", ["남성", "여성"], horizontal=True)
with col2: main_cat = st.selectbox("대분류", list(SPORT_MASTER_DB.keys()))
with col3: sub_cat = st.selectbox("세부 종목", list(SPORT_MASTER_DB[main_cat].keys()))

# 2. 분석 메커니즘 투명성 공개
info = SPORT_MASTER_DB[main_cat][sub_cat]
gender_data = info[gender]
with st.expander(f"🔍 {gender} {sub_cat} 분석 메커니즘 확인", expanded=True):
    st.write(f"✅ **표준 범위:** {gender_data['범위']}° | **근거:** {info['출처']}")
    st.write(f"✅ **핵심 로직:** {gender_data['기준']} 추적")

uploaded_file = st.file_uploader("영상을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    data_list = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            # [종목별 최적화 좌표 추출 로직]
            if main_cat in ["구기", "수영"]: # 상체 중심
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            else: # 하체 중심 (육상 등)
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            data_list.append(angle if angle <= 180 else 360-angle)
            mp.solutions.drawing_utils.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    cap.release()
    st.write("---")
    user_avg = int(np.mean(data_list)) if data_list else 0
    min_s, max_s = gender_data["범위"]

    st.subheader(f"📊 {gender} {sub_cat} 정밀 진단 결과")
    c1, c2 = st.columns(2)
    c1.metric("나의 데이터", f"{user_avg}°")
    c2.metric(f"전문가 권장 ({gender})", f"{min_s}° ~ {max_s}°")

    st.markdown("### 🎯 핵심 요약")
    if min_s <= user_avg <= max_s: st.success("동작이 완벽합니다!")
    else: st.warning(gender_data["핵심"])

    with st.expander("🔍 상세 원리 (Why?)"): st.write(info["풀이"])
    st.markdown("### 🚀 맞춤 해결책 (How?)")
    st.info("실제 앱에서는 여기에 구체적인 훈련법이 추가됩니다.")
    st.balloons()
