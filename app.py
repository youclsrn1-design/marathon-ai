import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile

# 1. AI 초고속 엔진 설정
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 2. [초경량 스포츠 백과사전] - 대표님 기획: 종목명(분석부위) 패턴화
# 모든 종목은 상체, 하체, 전신 3가지 역학 패턴으로 수렴합니다.
SPORT_CATEGORIES = {
    "🏃‍♂️ 육상 (트랙 & 필드)": [
        "마라톤/장거리 (하체: 골반-무릎-발목)",
        "중거리/800m-1500m (하체: 골반-무릎-발목)",
        "단거리/허들 (하체: 골반-무릎-발목)",
        "장대높이뛰기 (전신: 어깨-골반-발목)",
        "도약/멀리뛰기 (하체: 골반-무릎-발목)",
        "투척/창·포환던지기 (상체: 어깨-팔꿈치-손목)"
    ],
    "🎯 동계 & 타겟 (빙상/설상/사격)": [
        "스피드스케이팅 (하체: 골반-무릎-발목)",
        "쇼트트랙 (하체: 골반-무릎-발목)",
        "바이애슬론 (전신: 어깨-골반-발목)",
        "사격/권총·소총 (상체: 어깨-팔꿈치-손목)",
        "양궁 (상체: 어깨-팔꿈치-손목)"
    ],
    "🏐 구기 & 라켓 (코트/필드)": [
        "축구 슈팅/패스 (하체: 골반-무릎-발목)",
        "농구 점프슛 (상체: 어깨-팔꿈치-손목)",
        "배구 스파이크/서브 (상체: 어깨-팔꿈치-손목)",
        "핸드볼 슛 (전신: 어깨-골반-발목)",
        "테니스 포핸드/서브 (상체: 어깨-팔꿈치-손목)",
        "배드민턴 스매시 (상체: 어깨-팔꿈치-손목)",
        "탁구 드라이브 (하체: 골반-무릎-발목)",
        "야구 투구 (상체: 어깨-팔꿈치-손목)",
        "야구 타격 (전신: 어깨-골반-발목)"
    ],
    "🥋 무도 & 수상 (격투/수영)": [
        "복싱 펀치/가드 (상체: 어깨-팔꿈치-손목)",
        "유도 메치기/업어치기 (전신: 어깨-골반-발목)",
        "태권도 발차기 (하체: 골반-무릎-발목)",
        "수영 4대 영법 (상체: 어깨-팔꿈치-손목)"
    ]
}

# 공통 피드백 가이드 (성별/부위별 10초 컷 핵심 분석)
FEEDBACK_GUIDE = {
    "상체": {"남성": (90, 160, "파워 전달을 위한 관절의 확장성 부족"), "여성": (85, 155, "유연성을 활용한 최대 가동 범위 미달")},
    "하체": {"남성": (140, 180, "지면 반발력을 위한 하체 지지력 약화"), "여성": (135, 175, "코어-하체 연결부의 안정성 저하")},
    "전신": {"남성": (160, 180, "전신 협응력을 위한 수직/수평 정렬 붕괴"), "여성": (155, 175, "운동 에너지 전이를 위한 신체 밸런스 흔들림")}
}

st.set_page_config(page_title="ATHLETES AI PRO", layout="wide")
st.title("⚡ ATHLETES AI: 초고속 실시간 패턴 분석기")

# 3. 직관적인 UI (성별 -> 대분류 -> 세부종목)
col1, col2, col3 = st.columns(3)
with col1: gender = st.radio("👤 성별", ["남성", "여성"], horizontal=True)
with col2: main_cat = st.selectbox("분류", list(SPORT_CATEGORIES.keys()))
with col3: sub_cat = st.selectbox("종목 (분석 타겟)", SPORT_CATEGORIES[main_cat])

# 타겟 부위 자동 파악 로직 ("상체", "하체", "전신" 추출)
target_part = "하체" # 기본값
if "상체" in sub_cat: target_part = "상체"
elif "전신" in sub_cat: target_part = "전신"

min_s, max_s, core_msg = FEEDBACK_GUIDE[target_part][gender]

with st.expander(f"👓 실시간 AI 추적 세팅 완료: [{target_part}] 포커스", expanded=True):
    st.write(f"✅ **선택 종목:** {sub_cat}")
    st.write(f"✅ **{gender} 임계 범위:** {min_s}° ~ {max_s}°")
    st.info("💡 10초 이내에 핵심 관절의 패턴을 추출하여 화면에 표시합니다.")

uploaded_file = st.file_uploader("영상을 업로드하세요. 즉시 분석이 시작됩니다.", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    cap = cv2.VideoCapture(tfile.name)
    
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
            
            # 4. [핵심] 괄호 안의 지시어에 따른 초고속 분기 처리
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
            
            # 수학적 앵글 계산 (패턴화)
            angle = np.abs(np.degrees(np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])))
            curr_angle = int(angle if angle <= 180 else 360-angle)
            data_list.append(curr_angle)
            
            # AR 오버레이
            cv2.putText(image, f"{target_part.upper()} ANGLE: {curr_angle}deg", (30, 60), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)

        frame_window.image(image, channels="RGB")
        status_text.text(f"⚡ 실시간 {target_part} 패턴 분석 중... 현재 각도: {curr_angle if data_list else 0}°")

    cap.release()
    st.write("---")
    
    # 5. 핵심 브리핑 리포트
    user_avg = int(np.mean(data_list)) if data_list else 0
    
    st.subheader(f"📊 {sub_cat.split('(')[0].strip()} 핵심 요약 리포트")
    c1, c2, c3 = st.columns(3)
    c1.metric("타겟 부위", target_part)
    c2.metric("내 측정 평균", f"{user_avg}°")
    c3.metric("성별 기준 범위", f"{min_s}° ~ {max_s}°")

    if min_s <= user_avg <= max_s:
        st.success("✅ [정상 패턴] 해당 종목의 역학적 밸런스가 매우 우수합니다.")
    else:
        st.error(f"⚠️ [패턴 이탈] {core_msg}")
        st.info("💡 실시간 AR 글래스를 통해 해당 부위의 궤적을 수정하세요.")
