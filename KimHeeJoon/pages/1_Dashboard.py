import streamlit as st
import pandas as pd

st.title("📊 Overview Dashboard")

# 예시 값 (실제론 모델 예측 결과로 대체)
total_users = 100_000
churn_users = 12_340
avg_proba = 0.23
high_risk_ratio = 0.08

col1, col2, col3, col4 = st.columns(4)

col1.metric("전체 사용자 수", f"{total_users:,}")
col2.metric("이탈 위험 사용자", f"{churn_users:,}")
col3.metric("평균 이탈 확률", f"{avg_proba:.2f}")
col4.metric("High Risk 비율", f"{high_risk_ratio:.2%}")

st.divider()
st.subheader("📈 이탈 확률 분포 (예시)")
st.caption("모델 예측 결과 기반 시각화 영역")
