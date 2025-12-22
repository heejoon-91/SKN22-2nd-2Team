
import streamlit as st
import pandas as pd
import textwrap
import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir / "src"))

from ui_components import header, subheader, card, apply_global_styles, metric_card

st.set_page_config(
    page_title="KKBox Churn Control Center",
    page_icon="📊",
    layout="wide"
)

def main():
    header("analytics", "KKBox 구독 이탈 관리 시스템 (Churn Control Center)")
    apply_global_styles()
    st.subheader("팩트 기반의 데이터 설계를 통한 예측 신뢰도 확보")
    
    st.divider()
    
    # 1.1 Data Boundary
    subheader("calendar_today", "1.1 데이터 분석 바운더리 (Analysis Boundary)")
    
    # Row 1
    col_r1_1, col_r1_2 = st.columns(2)
    with col_r1_1:
        metric_card("event", "기준 시점 (Target Date)", "2017-04-01", "모델 예측 및 데이터 집계의 기준일(T)", "#1976D2")
    with col_r1_2:
        metric_card("warning", "이탈 정의 (Churn)", "만료 후 30일 미결제", "비즈니스 표준에 따른 이탈 확정 기준", "#E65100", "#FFF3E0")
        
    # Row 2
    col_r2_1, col_r2_2 = st.columns(2)
    with col_r2_1:
        metric_card("history_edu", "이력 집계 (History)", "가입 시점 ~ T", "전체 결제 및 구독 라이프사이클 분석", "#43A047")
    with col_r2_2:
        metric_card("timelapse", "행동 집계 (Behavior w30)", "2017-03-01 ~ 03-31", "T 기준 과거 30일 단기 행동 집중 분석", "#1565C0", "#E3F2FD")
    
    st.divider()
    
    # 1.2 Feature Spec
    subheader("settings_suggest", "1.2 핵심 지표 계산식 (Feature Specification)")
    st.caption("비즈니스 가치가 검증된 주요 파생 변수 명세입니다.")
    
    features = [
        {"구분": "행동", "파생 지표명": "active_decay_rate", "비즈니스 가치": "한 달 평균 대비 최근 1주 활동 급감 추세"},
        {"구분": "행동", "파생 지표명": "listening_velocity", "비즈니스 가치": "직전 2주간의 청취 가속도 (이탈 전조 현상)"},
        {"구분": "행동", "파생 지표명": "skip_passion_index", "비즈니스 가치": "서비스 만족도 및 콘텐츠 매칭 정확도 하락 지표"},
        {"구분": "환경", "파생 지표명": "subscription_months", "비즈니스 가치": "유저의 누적 서비스 충성도 및 LTV 잠재력"}
    ]
    st.table(pd.DataFrame(features))

    st.divider()
    st.markdown("""
    <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; border: 1px solid #90CAF9;">
        <div style="display: flex; align-items: center;">
            <span class="material-icons" style="color: #1976D2; margin-right: 10px;">info</span>
            <span style="color: #0D47A1; font-weight: 500;">왼쪽 사이드바에서 <strong>Model Guideline</strong>, <strong>Model Explainability</strong>, <strong>Risk Matrix</strong>, <strong>Marketing Simulator</strong> 메뉴를 차례로 확인해보세요.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
