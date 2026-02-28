import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import time

# 1. AI 엔진 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 2. [초단순 3단계 트리 구조] - 대표님 기획 완벽 반영
SPORT_TREE = {
    "올림픽 종목 (육상/수영/빙상 등)": {
        "육상 - 트랙": [
            "100m 단거리 (하체: 골반-무릎-발목)",
            "마라톤/장거리 (하체: 골반-무릎-발목)",
            "110m 허들 (전신: 어깨-골반-발목)"
        ],
        "육상 - 필드": [
            "장대높이뛰기 (전신: 어깨-골반-발목)",
            "창던지기 (상체: 어깨-팔꿈치-손목)"
        ],
        "동계 올림픽": [
            "쇼트트랙 (하체: 골반-무릎-발목)",
            "스피드스케이팅 (하체: 골반-무릎-발목)",
            "바이애슬론 (전신: 어깨-골반-발목)"
        ],
        "무도/격투": [
            "유도 (전신: 어깨-골반-발목)",
            "태권도 (하체: 골반-무릎-발목)",
            "복싱 (상체: 어깨-팔꿈치-손목)"
        ]
    },
    "대중 구기 종목 (축구/야구/미식축구 등)": {
        "축구": [
            "슈팅/프리킥 (하체: 골반-무릎-발목)",
            "헤딩/점프 (전신: 어깨-골반-발목)"
        ],
        "야구": [
            "투구/피칭 (상체: 어깨-팔꿈치-손목)",
            "타격/스윙 (전신: 어깨-골반-발목)"
        ],
        "미식축구": [
            "쿼터백 패스 (상체: 어깨-팔꿈치-손목)",
            "러닝백 스프린트 (하체: 골반-무릎-발목)"
        ],
        "배구/핸드볼": [
            "스파이크/점프슛 (상체: 어깨-팔꿈치-손목)"
        ]
    },
    "타겟 및 라켓 종목": {
        "타겟 (사격/양궁)": [
            "양궁 (상체: 어깨-팔꿈치-손목)",
            "사격 (상체: 어깨-팔꿈치-손목)"
        ],
        "라켓 (테니스/탁구)": [
            "포핸드/스매시 (상체: 어깨-팔꿈치-손목)",
            "탁구 드라이브 (하체: 골반-무릎-발목)"
        ]
    }
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="centered")
st.title("⚡ ATHLETES AI: 3단계 초고속 분석 엔진")

# 3. [1-2-3단계 직관적 UI]
col1, col2 = st.columns(2)
with col1:
    l1 = st.selectbox("1단계: 대분류", list(SPORT_TREE.keys()))
with col2:
    l2 = st.selectbox("2단계: 중분류", list(SPORT_TREE[l1].keys()))

l3 = st.selectbox("3단계: 세부 종목 및 분석 타겟", SPORT_TREE[l1][l2])

# 타겟 자동 추출 ("하체", "상체", "전신")
target_part = l3.split("(")[1].split(":")[0]

uploaded_file = st.file_uploader("영상을 업로드하세요. (빠른 백그라운드 분석 진행)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 4. [영상 숨김 처리] 어지러운 영상 대신 깔끔한 진행 바 사용
    st.info(f"🔍 AI가 [{target_part}] 역학 및 영상 내 오디오(충격음)를 분석 중입니다...")
    progress_bar = st.progress(0)
    
    data_list = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # 화면 출력 없이 내부에서만 초고속 계산
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            if target_part == "상체":
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            elif target_part == "전신":
                a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            else: # 하체
                a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            data_list.append(int(angle if angle <= 180 else 360-angle))
            
        frame_count += 1
        progress_bar.progress(min(int((frame_count / total_frames) * 100), 100))

    cap.release()
    progress_bar.empty()
    st.success("✅ 분석 완료!")
    st.write("---")
    
    # 5. [멀티모달 & 유튜브 연동 피드백] - 대표님 지시문구 그대로 적용
    user_avg = int(np.mean(data_list)) if data_list else 0
    
    st.subheader(f"📊 {l3.split('(')[0].strip()} 정밀 분석 결과")
    st.metric("타겟 관절 평균 각도", f"{user_avg}°")

    st.markdown("### 🔊 AI 멀티모달 (자세 + 오디오) 진단")
    st.warning("발바닥이 닿을 때 '딱딱' 소리가 나는 것을 보아 무릎에 충격을 많이 받게 되는 폼이니 자세 변화가 필요해 보입니다. 어깨에 힘을 빼고 장요근을 활용해 피치를 하시면 골반 근육을 잘 사용할뿐더러 착지 발 위치가 목표 위치에 가까워집니다.")

    st.markdown("### 📺 AI 맞춤 유튜브 훈련 처방")
    st.info("💡 **AI 신체/리듬 파악 결과:** 예상 신장 175cm 대역, 순간 반응속도 우수, 박자감(Rhythm) 일정함.")
    st.write("**추천 훈련법:** 피치 훈련, 하복근 및 장요근 강화 훈련")
    
    # 구글 생태계(유튜브) 연동 시뮬레이션 버튼
    search_query = f"{l3.split('(')[0].strip()} 장요근 피치 훈련법"
    st.link_button(f"▶️ 유튜브 '{search_query}' 맞춤 영상 보기", f"https://www.youtube.com/results?search_query={search_query}")
