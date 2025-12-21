import streamlit as st
import pandas as pd
import numpy as np

st.title("📋 High Risk 사용자 목록")

threshold = st.slider("이탈 확률 Threshold", 0.0, 1.0, 0.7)

df = pd.DataFrame({
    "user_id": range(1, 101),
    "churn_proba": np.random.rand(100)
})

high_risk_df = df[df["churn_proba"] >= threshold]

st.write(f"고위험 사용자 수: {len(high_risk_df)}명")
st.dataframe(high_risk_df.sort_values("churn_proba", ascending=False))
