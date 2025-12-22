import streamlit as st
import pandas as pd

# -----------------------
# Page 설정
# -----------------------
st.set_page_config(
    page_title="이탈 위험군 분류",
    layout="wide"
)

st.title("🚨 이탈 위험군 분류")

# -----------------------
# 세션 데이터 체크
# -----------------------
if "synthetic_pred_df" not in st.session_state:
    st.warning("먼저 샘플 데이터를 생성하고 예측을 수행해주세요.")
    st.stop()

# 원본 데이터 (절대 수정하지 않음)
df = st.session_state["synthetic_pred_df"]

st.subheader("① 예측 완료 데이터 미리보기")
st.dataframe(df.head())

# -----------------------
# 위험군 기준 설정
# -----------------------
st.subheader("② 위험군 기준 설정")

high_th = st.slider(
    "High Risk 기준 (이상)",
    min_value=0.5,
    max_value=0.9,
    value=0.7,
    step=0.05
)

mid_th = st.slider(
    "Medium Risk 기준 (이상)",
    min_value=0.2,
    max_value=high_th,
    value=0.4,
    step=0.05
)

# -----------------------
# 위험군 재계산 (항상 새로)
# -----------------------
def assign_risk(p, high, mid):
    if p >= high:
        return "High"
    elif p >= mid:
        return "Medium"
    else:
        return "Low"

df_view = df.copy()
df_view["risk_group"] = df_view["churn_probability"].apply(
    lambda x: assign_risk(x, high_th, mid_th)
)

# -----------------------
# 위험군 분포 시각화
# -----------------------
st.subheader("③ 위험군 분포")
st.bar_chart(
    df_view["risk_group"].value_counts()
)

# -----------------------
# High Risk 고객 표시
# -----------------------
st.subheader("④ High Risk 고객 리스트")

high_risk_df = (
    df_view[df_view["risk_group"] == "High"]
    .sort_values("churn_probability", ascending=False)
)

st.dataframe(high_risk_df)

# -----------------------
# 요약 정보
# -----------------------
st.subheader("⑤ 위험군 요약")

summary_df = (
    df_view["risk_group"]
    .value_counts()
    .rename("count")
    .to_frame()
)

st.dataframe(summary_df)
