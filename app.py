# 🎙️ [초경량 버전] 종목별 맞춤 피드백 (메모리 최적화)
def get_supreme_report(sport, gender, target, angle):
    clean_target = "Global" if "Global" in target else "Korea"
    try:
        ref = ELITE_DB[sport][gender][clean_target]
    except:
        ref = 170 
        
    diff = angle - ref
    
    report = f"### 📊 [AI 초정밀 역학 진단: {sport}]\n\n"
    report += f"**1. 수치 분석:** 측정 각도 **{angle}°** (엘리트 기준 {ref}° 대비 {abs(diff)}° 차이)\n\n"

    if abs(diff) <= 2:
        report += "**2. 결과:** 완벽한 역학적 상태입니다. 힘의 손실이 없습니다.\n"
    elif sport == "마라톤":
        if diff < 0:
            report += "**2. 원인:** 무릎이 과도하게 굽혀져 에너지가 낭비되고 있습니다.\n"
        else:
            report += "**2. 원인:** 착지 시 무릎이 펴져 있어 장경인대 부상 위험이 있습니다.\n"
    elif sport == "경보":
        if diff < 0:
            report += "**2. 🚨 경고:** Knee-lock 규정 위반으로 파울(Bent Knee) 위험이 높습니다!\n"
        else:
            report += "**2. 원인:** 과신전이 발생하여 햄스트링에 무리가 갈 수 있습니다.\n"

    return report
