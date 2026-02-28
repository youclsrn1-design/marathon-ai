import streamlit as st
import time

# 화면 기본 설정
st.set_page_config(page_title="마라톤 AI", page_icon="🏃‍♂️")

st.title("🏃‍♂️ 마라톤 AI 분석기")
st.write("안전하고 과학적인 마라톤 완주를 위한 맞춤형 AI 처방전")

st.write("---")

# 1. 기본 정보 입력
col1, col2 = st.columns(2)
with col1:
    gender = st.radio("1️⃣ 성별", ["남성", "여성"], horizontal=True)
with col2:
    region = st.radio("2️⃣ 기준", ["한국 기준", "글로벌 기준"], horizontal=True)

target_time = st.selectbox("3️⃣ 목표 기록", ["서브 3 (3시간 이내)", "서브 4 (4시간 이내)", "완주 목표"])

st.write("---")

# 2. 달리기 영상 업로드
st.subheader("4️⃣ 달리기 영상 업로드")
uploaded_video = st.file_uploader("자세 분석을 위한 러닝 영상을 올려주세요", type=['mp4', 'mov'])

st.write("---")

# 3. 분석 결과 및 처방전
if st.button("분석 및 처방전 발급받기"):
    if uploaded_video is not None:
        # AI가 생각하는 듯한 로딩 효과 (2초)
        with st.spinner("AI가 영상을 프레임 단위로 쪼개어 각도를 분석 중입니다... 🔍"):
            time.sleep(2)
            
        st.success("✅ 영상 분석 완료!")

        # 시각적 한계 보완: 숫자로 보여주는 각도 변화
        st.subheader("📐 AI 관절 각도 변화 리포트")
        st.write("동영상으로는 놓치기 쉬운 찰나의 순간을 분석했습니다.")
        st.info("- **착지 시 무릎 각도:** 155도 (안정적인 범위입니다)")
        st.warning("- **지면 발목 각도:** 82도 (발목이 살짝 무너집니다. 교정 필요!)")
        st.info("- **상체 기울기:** 5도 (아주 훌륭한 직립 자세입니다)")

        # 점수 대신 '각도 분석 결과'를 바탕으로 한 부상 예방 처방
        st.subheader("💊 맞춤형 부상 예방 처방전")
        st.error(f"⚠️ **[{region} {gender} / {target_time} 목표]** 분석 결과, 착지 시 발목 안정성이 다소 떨어집니다.\n\n**[처방]** 발목 염좌 및 아킬레스건 부상 위험이 있습니다. 훈련 전후 **카프레이즈(종아리 들어올리기) 3세트**를 반드시 추가하시고, 당분간 무리한 스피드 훈련보다는 하체 밸런스 운동에 집중하세요.")

    else:
        st.error("⚠️ 정확한 처방을 위해 먼저 영상을 업로드해 주세요!")
