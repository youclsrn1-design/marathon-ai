# 🎙️ [Supreme 리포트 생성기] 종목/각도별 동적 맞춤 피드백 적용 버전
def get_supreme_report(sport, gender, target, angle):
    # 에러 방지용: "Global Elite"가 들어와도 "Global"만 추출해서 안전하게 매칭
    clean_target = "Global" if "Global" in target else "Korea"
    
    try:
        ref = ELITE_DB[sport][gender][clean_target]
    except KeyError:
        ref = 170 # 최후의 안전장치
        
    diff = angle - ref
    
    # 1. 수치 분석 (동일)
    report = f"### 📊 [AI 초정밀 역학 진단: {sport}]\n\n"
    report += f"**1. 수치 분석 (Fact Check)**\n측정된 피크 각도는 **{angle}°**입니다. {gender} {clean_target} 엘리트 기준({ref}°) 대비 **{abs(diff)}° {'차이' if abs(diff)>2 else '거의 일치'}**를 보입니다.\n\n"

    # 2 & 3. 종목 및 각도에 따른 동적 피드백 생성
    root_cause = ""
    metaphor = ""
    english = ""

    # [케이스 1] 완벽한 자세 (오차 2도 이내)
    if abs(diff) <= 2:
        root_cause = "지면 접촉 시 하체 관절의 정렬이 엘리트 선수들과 매우 흡사한 **최적의 역학적 상태**입니다. 힘의 손실 없이 지면 반발력을 100% 추진력으로 전환하고 있습니다."
        metaphor = "마치 '잘 조율된 스포츠카'처럼 완벽한 서스펜션을 보여주고 있습니다. 현재의 폼을 기억하고 유지하는 데 집중하세요."
        english = f"Perfect! Your knee angle ({angle}°) is perfectly matching the elite standard. Keep up the great work!"
        
    # [케이스 2] 마라톤 분석
    elif sport == "마라톤":
        if diff < 0: # 무릎이 너무 많이 굽혀짐
            root_cause = "착지 시 무릎이 너무 많이 굽혀져('Over-bending'), 몸의 무게를 뼈가 아닌 근육이 다 받아내고 있습니다. 이로 인해 에너지가 낭비되고 무릎에 과부하가 걸립니다."
            metaphor = "마치 '바람 빠진 타이어'로 달리는 것과 같습니다. 착지 순간 발목과 무릎을 조금 더 견고하게 버텨주세요."
            english = "Your knee is bending too much at impact. Try to keep your leg a bit stiffer to bounce off the ground efficiently."
        else: # 무릎이 너무 펴짐
            root_cause = "착지 시 무릎이 엘리트 기준보다 뻣뻣하게 펴져 있습니다. 충격이 흡수되지 못하고 관절로 그대로 전달되어 **장경인대염 등 부상 위험**이 높습니다."
            metaphor = "마치 '브레이크를 밟으며 달리는 것'과 같습니다. 발을 몸통보다 너무 멀리 뻗지 말고, 몸의 무게중심 바로 아래에 착지하세요."
            english = "Your knee is too straight. This acts like a brake and increases injury risk. Land your foot closer to your body's center."
            
    # [케이스 3] 경보 분석
    elif sport == "경보":
        if diff < 0: # 무릎이 굽혀짐 (파울)
            root_cause = "**[🚨 파울 주의]** 경보의 핵심 규정인 'Knee-lock(스트레이트 레그)'이 이루어지지 않아 **파울(Bent Knee) 판정 위험**이 매우 높습니다. 지면 추진력 또한 상실되고 있습니다."
            metaphor = "마치 '무너지는 다리'를 건너는 것과 같습니다. 뒷꿈치가 닿는 순간부터 수직이 될 때까지 무릎을 뒤로 쫙 펴서 잠가(Lock) 주셔야 합니다."
            english = "Warning: Foul risk! In race walking, your knee must be straightened (locked) from first contact until the vertical upright position."
        else: # 과신전
            root_cause = "무릎 펴짐 규정은 잘 준수하고 있으나, 관절이 뒤로 무리하게 꺾이는 과신전(Hyperextension)이 약간 발생하여 햄스트링에 무리가 갈 수 있습니다."
            metaphor = "규정은 통과했지만, 다리가 팽팽한 '활시위'처럼 한계치까지 꺾여 있습니다. 코어에 힘을 주어 골반으로 충격을 분산하세요."
            english = "Good knee lock, but slightly hyperextended. Engage your core to protect your hamstrings and distribute the impact."

    # 리포트에 합치기
    report += f"**2. 논리적 원인 분석 (Root Cause)**\n{root_cause}\n\n"
    report += f"**3. 💡 AI 코치의 비유 (Metaphor)**\n{metaphor}\n\n"
    report += f"> 🇺🇸 **Easy English:** {english}"

    return report
