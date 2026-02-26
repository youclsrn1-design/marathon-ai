import streamlit as st

# 화면을 넓게 쓰기 위한 기본 설정
st.set_page_config(page_title="AI 러닝 폼 분석기", layout="wide")

st.title("🏃‍♂️ AI 러닝 폼 분석 & 코칭 플랫폼 (MVP)")
st.markdown("---")

# 화면을 7:3 비율로 분할 (좌측: 분석/커뮤니티, 우측: 커머스/후원)
col1, col2 = st.columns([7, 3])

# ==========================================
# [좌측 영역 70%] AI 분석 및 커뮤니티
# ==========================================
with col1:
    tab1, tab2 = st.tabs(["🔍 AI 폼 분석기", "💬 러너스 커뮤니티"])
    
    with tab1:
        st.subheader("회원님의 달리기 영상을 올려주세요")
        uploaded_file = st.file_uploader("측면(Side-profile)에서 촬영된 영상 (MP4, MOV)", type=['mp4', 'mov'])
        
        c1, c2 = st.columns(2)
        with c1:
            gender = st.radio("성별 선택", ["남성", "여성"])
        with c2:
            standard = st.radio("비교 기준", ["🇰🇷 한국 엘리트 (현실적 목표)", "🌍 글로벌 엘리트 (극한의 목표)"])
            
        if st.button("분석 시작", type="primary"):
            if uploaded_file is None:
                st.error("⚠️ 영상을 먼저 업로드해 주세요!")
            else:
                st.info("비디오 분석 중... (관절 뼈대 트래킹 진행)")
                st.success("💡 [분석 결과] 목표 기준치보다 무릎 굽힘이 부족합니다. 스윙 시 발뒤꿈치를 조금 더 당겨 올려보세요.")

    with tab2:
        st.subheader("오늘의 러닝 폼 자랑하기")
        user_name = st.text_input("닉네임")
        user_comment = st.text_area("분석 결과를 바탕으로 질문이나 소감을 남겨주세요.")
        if st.button("게시글 등록"):
            st.success("등록되었습니다!")
        st.markdown("---")
        st.markdown("**초보러너** 🗣️: 무릎 각도 110도 나왔는데 어떻게 교정하나요?")
        st.markdown("**마라톤매니아** 🗣️: 오늘 케이던스 195 달성! 메타 안경 피드백 최고네요.")

# ==========================================
# [우측 영역 30%] 커머스 및 후원
# ==========================================
with col2:
    st.subheader("🛍️ Runner's Store")
    
    st.image("https://dummyimage.com/400x200/cccccc/000000&text=Meta+Smart+Glasses", use_column_width=True)
    st.markdown("**메타 레이밴 스마트 글래스 (직구)**\n\n실시간 음성 자세 교정 피드백")
    st.markdown("💰 **450,000원**")
    
    # ⬇️ 나중에 광고주 링크가 생기면 여기 주소를 바꾸시면 됩니다!
    st.link_button("장바구니 담기 🛒", "https://www.원하는광고주웹사이트.com")
    
    st.markdown("---")
    
    st.subheader("☕ 서버비 후원하기")
    st.info("이 무료 AI 분석기가 도움이 되셨나요? \n\n여러분의 작은 후원이 더 나은 자세 교정 AI를 만듭니다!")
    
    # ⬇️ 나중에 토스 송금 링크 등을 넣으시면 됩니다!
    st.link_button("토스(Toss) 익명 송금하기 💸", "https://toss.me/원하는아이디")
