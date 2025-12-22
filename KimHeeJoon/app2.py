import numpy as np
import pandas as pd
import streamlit as st
import joblib
import time

# -----------------------
# Synthetic Data 생성 함수
# -----------------------
def generate_synthetic_data(sample_df: pd.DataFrame, cat_cols, num_cols, n: int = 100):
    synth = {}

    for col in sample_df.columns:
        if col in num_cols:
            min_v = sample_df[col].min()
            max_v = sample_df[col].max()

            if min_v == max_v:
                synth[col] = np.repeat(min_v, n)
            else:
                synth[col] = np.random.uniform(min_v, max_v, n)

        elif col in cat_cols:
            synth[col] = np.random.choice(
                sample_df[col].astype(str).unique(),
                size=n
            )

    return pd.DataFrame(synth)



# -----------------------
# Streamlit 기본 설정
# -----------------------
st.set_page_config(
    page_title="KKBOX 이탈 예측",
    layout="wide"
)

st.title("🎧 KKBOX 이탈 예측 (Synthetic Data 생성 기반)")


# -----------------------
# 모델 로드
# -----------------------
@st.cache_resource
def load_model():
    return joblib.load("model/catboost_model.joblib")

bundle = load_model()

model = bundle["model"]
feature_cols = bundle["feature_cols"]
cat_cols = bundle["cat_cols"]
num_cols = bundle["num_cols"]




# -----------------------
# 기준 샘플 로드 (실제 데이터 head 5)
# -----------------------
@st.cache_data
def load_base_sample():
    return pd.read_csv("sample/kkbox_head_5.csv")

base_df = load_base_sample()

st.subheader("① 기준 데이터 (실제 학습 데이터 Head 5)")
st.dataframe(base_df)


# -----------------------
# Synthetic 데이터 생성
# -----------------------
st.subheader("② 동일 스키마 신규 샘플 데이터 생성")

if st.button("🧪 신규 샘플 100개 생성"):
    st.session_state["synthetic_df"] = generate_synthetic_data(
        base_df,
        cat_cols=cat_cols,
        num_cols=num_cols,
        n=10000
    )


if "synthetic_df" in st.session_state:
    synthetic_df = st.session_state["synthetic_df"]

    # CatBoost categorical 안전 처리
    for col in cat_cols:
        synthetic_df[col] = synthetic_df[col].astype(str)

    st.subheader("③ 생성된 Synthetic 데이터 미리보기")
    st.dataframe(synthetic_df.head())

    # -----------------------
    # 이탈 확률 예측
    # -----------------------
    X_pred = synthetic_df[feature_cols]
    preds = model.predict_proba(X_pred)[:, 1]
    synthetic_df["churn_probability"] = preds

    # -----------------------
    # 결과 표시
    # -----------------------
    st.subheader("④ 이탈 확률 예측 결과 (상위 10건)")

    st.dataframe(
        synthetic_df
        .sort_values("churn_probability", ascending=False)
        .head(10)
    )

    # -----------------------
    # 요약 통계
    # -----------------------
    st.subheader("⑤ 이탈 확률 요약 통계")

    st.dataframe(
        synthetic_df["churn_probability"]
        .describe()
        .to_frame("value")
    )

    # -----------------------
    # 분포 시각화
    # -----------------------
    st.subheader("⑥ 이탈 확률 분포")

    dist = (
        synthetic_df["churn_probability"]
        .value_counts(bins=10)
        .sort_index()
        .reset_index()
    )

    dist.columns = ["prob_bin", "count"]
    dist["prob_bin"] = dist["prob_bin"].astype(str)

    st.bar_chart(
        dist.set_index("prob_bin")
    )

    # 예측 이후
    synthetic_df["churn_probability"] = preds

    # 다른 페이지에서 쓰기 위한 저장
    st.session_state["synthetic_pred_df"] = synthetic_df.copy()
