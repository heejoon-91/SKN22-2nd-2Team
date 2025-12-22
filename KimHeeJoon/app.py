import streamlit as st
import pandas as pd
import joblib

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(page_title="KKBOX 이탈 예측", layout="wide")

st.title("🎧 KKBOX 고객 이탈 예측")
st.caption("CatBoost 기반 이탈 확률 예측 모델")

# -----------------------
# 모델 로드
# -----------------------
@st.cache_resource
def load_model():
    return joblib.load("model/catboost_model.joblib")

model = load_model()

# -----------------------
# 샘플 CSV 로드 (기준 데이터)
# -----------------------
@st.cache_data
def load_sample():
    return pd.read_csv("sample/kkbox_head_5.csv")

sample_df = load_sample()

# -----------------------
# 1. 샘플 CSV 다운로드
# -----------------------
st.subheader("① 샘플 CSV 다운로드")

st.download_button(
    label="📥 실제 데이터 기반 샘플 CSV 다운로드",
    data=sample_df.to_csv(index=False),
    file_name="kkbox_sample_input.csv",
    mime="text/csv",
)

st.info(
    "이 샘플은 **모델 학습에 사용된 실제 데이터에서 추출한 예시**입니다.\n"
    "동일한 컬럼 구조로 CSV를 업로드해주세요."
)

# -----------------------
# 2. CSV 업로드
# -----------------------
st.subheader("② 예측할 CSV 업로드")

uploaded_file = st.file_uploader(
    "CSV 파일을 업로드하세요",
    type=["csv"]
)

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)

    st.write("업로드한 데이터 미리보기", input_df.head())

    # -----------------------
    # 컬럼 검증
    # -----------------------
    missing_cols = set(sample_df.columns) - set(input_df.columns)

    if missing_cols:
        st.error(f"필수 컬럼이 누락되었습니다: {missing_cols}")
        st.stop()

    # -----------------------
    # 3. 예측
    # -----------------------
    if st.button("🚀 이탈 확률 예측"):
        preds = model.predict_proba(input_df)[:, 1]
        input_df["churn_probability"] = preds

        st.success("예측 완료")
        st.write(input_df[["churn_probability"]].head())

        # 결과 다운로드
        st.download_button(
            label="📥 예측 결과 다운로드",
            data=input_df.to_csv(index=False),
            file_name="kkbox_churn_prediction.csv",
            mime="text/csv",
        )
