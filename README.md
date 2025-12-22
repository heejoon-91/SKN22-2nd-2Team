# KKBox 구독 이탈 관리 시스템 (Churn Control Center)

## 프로젝트 개요
본 프로젝트는 **KKBox** 음원 스트리밍 서비스의 사용자 이탈을 방지하고 구독 유지를 관리하기 위해 개발된 **이탈 예측 및 관리 시스템**입니다.
데이터 전처리, 파생 변수 생성, 머신러닝 모델링 과정을 거쳐 이탈 가능성이 높은 사용자를 조기에 식별하고, Streamlit 기반의 대시보드를 통해 비즈니스 인사이트를 제공합니다.


## SKN22-2nd-2Team "에용"
- 안민제, 임도형, 이규빈, 이도훈, 김희준
- 25.12.22

## 사용 기술 (Tech Stack)

### Languages & Libraries
<div align="left">
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white">
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">
  <img src="https://img.shields.io/badge/CatBoost-E9711C?style=for-the-badge&logo=CatBoost&logoColor=white">
  <img src="https://img.shields.io/badge/Optuna-5E87F5?style=for-the-badge&logo=lightning&logoColor=white">
</div>

### Dashboard & Visualization
<div align="left">
  <img src="https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white">
  <img src="https://img.shields.io/badge/seaborn-76B900?style=for-the-badge&logo=seaborn&logoColor=white">
  <img src="https://img.shields.io/badge/matplotlib-0B579E?style=for-the-badge&logo=matplotlib&logoColor=white">
</div>

### Development Environment
<div align="left">
  <img src="https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white">
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white">
</div>

## 분석 및 개발 프로세스 (Process)

### 1. 공통 데이터 전처리 (Data Preprocessing V3)
- **참고**: `notebooks/preprocessing/build_train_feature_table.ipynb`
- 대용량 로그 데이터(user_logs)와 결제 데이터(transactions)를 효율적으로 병합 및 집계하였습니다.
- 메모리 사용량을 최적화하기 위해 데이터 타입(int8, int16, int32, category)을 세밀하게 조정하였습니다 (V3 데이터셋 구축).

### 2. 파생 변수 생성 (Feature Engineering V4 & V5)
- **참고**: `notebooks/preprocessing/build_train_feature_v4.ipynb`, `03_trained_model/model_report.md`
- **V4 (Strategic Features)**: 단순 집계를 넘어선 전략적 파생 변수 생성.
    - `active_decay_rate`: 활동 감소율
    - `listening_velocity`: 청취 가속도
    - `skip_passion_index`: 스킵 성향 지수
- **V5.2 (Safe Context)**: 결제 상태(Status) 정보를 배제하고, 유저의 성향(Context)과 순수 행동 패턴에 집중하여 과적합을 방지하고 조기 경보 능력을 강화했습니다.

### 3. 모델 선정을 위한 실험 (Model Selection Experiments)
- **참고**: `notebooks/modeling/*_summary.ipynb`, `03_trained_model`
- **실험 모델**: Logistic Regression, RandomForest, XGBoost, LightGBM, MLP, CatBoost
- 각 모델별로 `notebooks/modeling/` 경로에서 하이퍼파라미터 튜닝 및 성능 실험을 수행하였으며, 결과 요약은 `_summary` 파일들에 기록되어 있습니다.
- **최종 선정**: **CatBoost** (범주형 변수 처리 우수, 과적합 방지, Robustness 입증)

#### 실험 결과 요약 (Experiment Summary)
> 모델별 성능 변화 (Delta vs Baseline e0)

![Experiment Summary](docs/images/experiment_summary.png)

위 그림은 Baseline(e0) 대비 각 모델의 실험 단계별 성능 변화(평균)를 보여줍니다. CatBoost는 전반적으로 안정적인 성능 유지(Accuracy, Recall)와 높은 재현율을 보여 최종 모델로 선정되었습니다.

### 4. 모델 학습 (Final Model Training)
- 정의된 파생변수(Feature)를 기반으로, **user_logs의 행동 데이터를 비중 있게 반영**하기 위해 두 가지 트랙으로 모델을 학습시켰습니다.
    - **V4 Model (High Precision)**: 결제 정보와 행동 정보를 모두 활용하여, 이미 이탈 징후가 뚜렷한(자동갱신 해지 등) 고위험군을 정밀 타겟팅합니다.
    - **V5.2 Model (Early Warning)**: 결제 상태를 가리고 순수 행동 패턴(청취 급감, 스킵 증가 등)만으로 학습하여, **구독은 유지 중이나 이탈 위험이 높은 잠재 이탈자**를 선제적으로 방어합니다.

> **💡 왜 두 개의 모델을 쓰나요? (Two-Track Strategy)**
> 결제 만료가 임박하거나 해지한 사용자(Active Churn)뿐만 아니라, **아직 돈은 내고 있지만 마음은 떠난 사용자(Silent Churn)를 놓치지 않기 위함**입니다. 이 두 모델의 시너지를 통해 빈틈없는 이탈 관리가 가능합니다.

## 📊 데이터 스키마 (Data Schema & Feature Summary)
모델 학습에 활용된 핵심 파생 변수(Derived Features) 요약입니다. (V4 Dataset 기준)

### 1. 이력 및 환경 변수 (History & Environment) - V4 Key Features
| 변수명 (Feature) | 설명 (Description) | 비즈니스 의미 |
| :--- | :--- | :--- |
| `days_since_last_cancel` | 최근 취소 경과일 | "이전에 해지한 적이 있는가?" (습관적 이탈) |
| `days_since_last_payment` | 결제 공백기 | "마지막 결제로부터 며칠이 지났는가?" (이탈 임박) |
| `is_auto_renew_last` | 자동 갱신 여부 | "자동 갱신을 켜두었는가?" (가장 강력한 방어선) |
| `subscription_months` | 구독 유지 기간 | "얼마나 오래 사용한 충성 고객인가?" |

### 2. 행동 변수 (User Behavior) - V5.2 Key Features
| 변수명 (Feature) | 설명 (Description) | 비즈니스 의미 |
| :--- | :--- | :--- |
| `active_decay_rate` | 활동 감소율 | "평소(30일) 대비 최근(7일) 접속이 얼마나 줄었는가?" |
| `listening_velocity` | 청취 가속도 | "최근 2주간 청취 시간이 급격히 줄어들고 있는가?" |
| `skip_passion_index` | 스킵 열정도 | "곡을 듣지 않고 넘기는 비율이 비정상적으로 높은가?" |
| `last_active_gap` | 마지막 활동 경과일 | "구독은 되어 있는데, 접속을 안 한지 며칠째인가?" |

### 5. 대시보드 구축 (Interactive Dashboard)
- **Streamlit**을 활용하여 예측 결과와 주요 지표를 시각화
- **주요 기능**:
    - Model Guideline
    - Model Explainability (Z-score 분석 등 V5.2 주요 변수 해석)
    - Risk Matrix
    - Marketing Simulator

---

## 프로젝트 구조 (Directory Structure)

```bash
SKN22-2nd-2Team
├── app.py                      # Streamlit Main App
├── requirements.txt            # Project Dependencies
├── data/                       # Data (Raw & Processed, Ignored in Git)
├── notebooks/                  # Jupyter Notebooks
│   ├── eda/                    # Exploratory Data Analysis
│   ├── preprocessing/          # Data Preprocessing & Feature Engineering
│   └── modeling/               # Model Training & Experiments
├── src/                        # Source Code
│   ├── preprocessing/          # Preprocessing Logic Modules
│   └── modeling/               # Model Pipeline Modules
├── pages/                      # Streamlit Pages
│   ├── 2_Model_Guideline.py
│   ├── 3_Model_Explainability.py
│   ├── 4_Risk_Matrix.py
│   └── 5_Marketing_Simulator.py
├── 01_preprocessing_report/    # Preprocessing Reports
├── 02_training_report/         # Model Training Reports
└── 03_trained_model/           # Model Artifacts & Reports
```

---

## 설치 및 실행 (Installation & Usage)

### 1. 요구 사항 (Requirements)
본 프로젝트는 Python 3.8+ 환경에서 실행을 권장합니다.
필요한 패키지는 `requirements.txt`에 명시되어 있습니다.

```bash
pip install -r requirements.txt
```

### 2. 실행 방법 (Usage)
Streamlit 대시보드를 실행하여 시스템을 확인할 수 있습니다.

```bash
streamlit run app.py
```

---