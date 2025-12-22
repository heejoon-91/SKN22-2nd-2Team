import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Setup Paths & Imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root / "src"))

from ui_components import header, subheader, section_header, apply_global_styles, card

def main():
    header("visibility", "이탈 예측 가이드라인 (Model Guideline)", "모델이 유저를 진단하는 기준과 마케팅 개입 포인트를 매칭합니다.")
    apply_global_styles()
    
    st.divider()

    # --- Section 1: Interactive Persona ---
    subheader("face", "1. 모델의 속마음 인터랙티브 (Interactive Persona)")
    st.markdown("유저의 행동 변화에 따라 모델이 위험도를 어떻게 판단하는지 **직접 체험**해보세요.")
    
    col_p1, col_p2 = st.columns([1.2, 1])
    
    with col_p1:
        section_header("accessibility_new", "유저 행동 시뮬레이션")
        st.caption("최근 유저에게 발생한 이벤트를 체크하세요.")
        
        check_decay = st.checkbox("최근 7일간 접속하지 않음 (Activity Decay)", value=True)
        check_skip = st.checkbox("평소보다 곡 스킵(Skip)이 2배 급증함", value=False)
        check_payment = st.checkbox("자동 결제 갱신일이 3일 남음", value=False)
        check_old = st.checkbox("가입한 지 3년 이상 된 장기 유저임", value=False)
        
    with col_p2:
        # Simple Scoring Logic
        score = 0
        reasons = []
        
        if check_decay: 
            score += 40
            reasons.append("접속 공백은 가장 강력한 이탈 신호입니다.")
        if check_skip: 
            score += 30
            reasons.append("만족도 저하(스킵)는 이탈 전조 현상입니다.")
        if check_payment: 
            score += 20
            reasons.append("갱신일 임박은 의사결정의 순간입니다.")
        if check_old: 
            score -= 20 # Loyalty bonus
            reasons.append("장기 유저는 충성도 점수로 위험이 감산됩니다.")
            
        # Normalize
        score = max(0, min(100, score))
        
        section_header("smart_toy", "모델의 실시간 판단")
        
        # 4 Segments Logic (Aligned with Page 3)
        if score >= 80:
            card("dangerous", f"위험 지대 (Danger): {score}점", 
                 ["판단: **'마음이 이미 떠났습니다.'**"] + reasons, 
                 "#FFEBEE", "#FF5252")
        elif score >= 50:
            card("warning", f"경보 지대 (Warning): {score}점", 
                 ["판단: **'고민하고 있는 단계입니다.'**"] + reasons, 
                 "#FFF3E0", "#FF9800")
        elif score >= 20:
             card("visibility", f"주의 지대 (Watch-out): {score}점", 
                 ["판단: **'활동이 뜸해지고 있습니다.'**"] + reasons, 
                 "#FFFDE7", "#FBC02D")
        else:
            card("verified", f"안전 지대 (Safe): {score}점", 
                 ["판단: **'서비스를 잘 즐기고 있습니다.'**"] + reasons, 
                 "#E8F5E9", "#4CAF50")

    st.divider()

    # --- Section 2: Signal Dictionary ---
    subheader("traffic", "2. 이탈 시그널 신호등 (Signal Dictionary)")
    st.caption("대시보드 지표를 보고 즉시 판단할 수 있는 가이드라인입니다.")
    
    col_danger, col_warning, col_watchout, col_safe = st.columns(4)
    
    with col_danger:
        card("dangerous", "위험 지대 (Danger)", 
             ["**기준**: Active Decay < 0.5", "의미: 평소 활동량의 절반 이하로 급감", "액션: 즉시 쿠폰/혜택 지급 필요"], 
             "#FFEBEE", "#FF5252")
        
    with col_warning:
        card("warning", "경보 지대 (Warning)", 
             ["**기준**: Listening Velocity 하락세", "의미: 청취 시간이 서서히 줄어듦", "액션: 결제 수단 업데이트 유도"], 
             "#FFF3E0", "#FF9800")
    
    with col_watchout:
        card("visibility", "주의 지대 (Watch-out)", 
             ["**기준**: Skip Count 증가", "의미: 접속은 하나 만족도가 떨어짐", "액션: 신규 콘텐츠/플레이리스트 푸시"], 
             "#FFFDE7", "#FBC02D")
        
    with col_safe:
        card("verified", "안전 지대 (Safe)", 
             ["**기준**: Completion Ratio > 0.8", "의미: 곡을 끝까지 듣는 비율 높음", "액션: 유지 (별도 개입 불필요)"], 
             "#E8F5E9", "#4CAF50")
             
    st.divider()

    # --- Section 3: Actionability Map ---
    subheader("touch_app", "3. 개입 가능성 리포트 (Actionability Map)")
    st.markdown("<strong>'어쩔 수 없는 것(Filter)'</strong>과 <strong>'바꿀 수 있는 것(Trigger)'</strong>을 구분해야 합니다.", unsafe_allow_html=True)
    
    # Mock Data for plotting
    data = {
        'Feature': ['가입 기간', '나이/성별', '결제 수단', '접속 빈도', '곡 스킵 수', '검색 횟수', '청취 시간'],
        'Contribution': [80, 40, 60, 85, 70, 50, 75], # X축: 모델 중요도
        'Actionability': [10, 5, 20, 80, 90, 85, 70], # Y축: 마케팅 개입 가능성
        'Type': ['환경/이력 (V4)', '환경/이력 (V4)', '환경/이력 (V4)', '행동 (V5.2)', '행동 (V5.2)', '행동 (V5.2)', '행동 (V5.2)']
    }
    df_map = pd.DataFrame(data)
    
    fig = px.scatter(df_map, x='Contribution', y='Actionability', 
                     color='Type', text='Feature',
                     color_discrete_map={'환경/이력 (V4)': '#90CAF9', '행동 (V5.2)': '#FFAB91'},
                     size=[30]*7, 
                     labels={'Contribution': '모델 예측 기여도 (Importance)', 'Actionability': '마케팅 개입 가능성 (Action)'})
    
    fig.update_traces(textposition='top center', textfont_size=14)
    fig.add_hline(y=50, line_dash="dash", line_color="gray")
    fig.add_vline(x=50, line_dash="dash", line_color="gray")
    
    # Quadrant Annotations
    fig.add_annotation(x=90, y=90, text="<b>Focus Zone</b><br>(중요하고 바꿀 수 있음)", showarrow=False, font=dict(color="#D84315"))
    fig.add_annotation(x=90, y=10, text="<b>Filtering Zone</b><br>(중요하지만 못 바꿈)", showarrow=False, font=dict(color="#1565C0"))
    
    fig.update_layout(height=500, margin=dict(t=30, b=30), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Replaced st.info with card
    card("lightbulb", "핵심 결론", 
         "**V4 변수(파란 점)**로 '타겟을 좁히고', **V5.2 변수(주황 점)**를 건드려 '행동을 변화'시켜야 합니다.",
         "#E3F2FD", "#2196F3", "#0D47A1")

if __name__ == "__main__":
    main()
