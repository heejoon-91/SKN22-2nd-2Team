import streamlit as st
import pandas as pd

st.title("🧠 Feature Importance")

st.caption("RandomForest / LightGBM 중요 변수")

# 예시 데이터
imp_df = pd.DataFrame({
    "feature": [f"feature_{i}" for i in range(10)],
    "importance": sorted([0.3,0.2,0.15,0.1,0.08,0.06,0.05,0.03,0.02,0.01], reverse=True)
})

st.bar_chart(imp_df.set_index("feature"))
