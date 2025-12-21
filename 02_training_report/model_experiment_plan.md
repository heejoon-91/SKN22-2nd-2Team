# KKBox Churn Prediction – Feature Ablation Experiment Plan (Detailed)

본 문서는 **Feature Ablation 실험의 목적, 실험 이유, 예상 결과**와 함께  
각 실험 단계(e0~e3.1)에서 **실제로 사용/제외되는 컬럼 목록을 팩트 기반으로 명시**한다.

---

## 공통 설정

```python
RANDOM_STATE = 719

ID_COL = "msno"
TARGET_COL = "is_churn"
```

---

## e0. 전체 컬럼 사용 (Baseline)

### 사용 목적
- 모델이 달성할 수 있는 **이론적 최대 성능 기준선** 확보
- 이후 모든 실험 결과 비교의 기준(anchor)

### 사용 컬럼

#### Categorical
```python
city
gender
registered_via
last_payment_method
has_ever_paid
has_ever_cancelled
is_auto_renew_last
is_free_user
```

#### Numerical
```python
reg_days

# w7
num_days_active_w7
total_secs_w7
avg_secs_per_day_w7
std_secs_w7
num_songs_w7
avg_songs_per_day_w7
num_unq_w7
num_25_w7
num_100_w7
short_play_w7
skip_ratio_w7
completion_ratio_w7
short_play_ratio_w7
variety_ratio_w7

# w14
num_days_active_w14
total_secs_w14
avg_secs_per_day_w14
std_secs_w14
num_songs_w14
avg_songs_per_day_w14
num_unq_w14
num_25_w14
num_100_w14
short_play_w14
skip_ratio_w14
completion_ratio_w14
short_play_ratio_w14
variety_ratio_w14

# w21
num_days_active_w21
total_secs_w21
avg_secs_per_day_w21
std_secs_w21
num_songs_w21
avg_songs_per_day_w21
num_unq_w21
num_25_w21
num_100_w21
short_play_w21
skip_ratio_w21
completion_ratio_w21
short_play_ratio_w21
variety_ratio_w21

# w30
num_days_active_w30
total_secs_w30
avg_secs_per_day_w30
std_secs_w30
num_songs_w30
avg_songs_per_day_w30
num_unq_w30
num_25_w30
num_100_w30
short_play_w30
skip_ratio_w30
completion_ratio_w30
short_play_ratio_w30
variety_ratio_w30

# trend
days_trend_w7_w14
secs_trend_w7_w30
secs_trend_w14_w30
days_trend_w7_w30
songs_trend_w7_w30
songs_trend_w14_w30
skip_trend_w7_w30
completion_trend_w7_w30

# transactions
days_since_last_payment
days_since_last_cancel
last_plan_days
total_payment_count
total_amount_paid
avg_amount_per_payment
unique_plan_count
subscription_months_est
payment_count_last_30d
payment_count_last_90d
```

### 예상 결과
- 최고 성능
- 일부 컬럼은 leakage 또는 운영 의존성 가능성 존재

---

## e1. 조건부 Leakage 위험 컬럼 제거

### 제외 컬럼
```python
days_since_last_payment
days_since_last_cancel
reg_days
is_auto_renew_last
```

### 실험 목적
- 라벨 시점과 직접적으로 연관될 수 있는 상태성/시간 파생 변수 제거
- 모델이 미래 정보에 의존하지 않는지 검증

### 예상 결과
- 성능 소폭 하락
- 하락 폭이 제한적일 경우, 행동 기반 학습 구조 확인

---

## e2. Transactions 컬럼 전체 제거 (Logs-only)

### 제외 컬럼
```python
days_since_last_payment
days_since_last_cancel
last_plan_days
total_payment_count
total_amount_paid
avg_amount_per_payment
unique_plan_count
subscription_months_est
payment_count_last_30d
payment_count_last_90d
```

### 실험 목적
- 결제 이력이 없는 사용자에도 적용 가능한 모델 여부 검증
- 행동 로그만으로 churn 신호 포착 가능성 확인

### 예상 결과
- ROC-AUC / PR-AUC 하락
- Recall 유지 시 조기 이탈 감지 모델로 실무 활용 가능

---

## e2.1. Transactions off + Leakage 위험 컬럼 제거

### 제외 컬럼
```python
# e2
days_since_last_payment
days_since_last_cancel
last_plan_days
total_payment_count
total_amount_paid
avg_amount_per_payment
unique_plan_count
subscription_months_est
payment_count_last_30d
payment_count_last_90d

# e1
reg_days
is_auto_renew_last
```

### 실험 목적
- 가장 보수적인 정보 구성
- 최소 정보 기반 모델 성능 하한선 확인

### 예상 결과
- 성능 추가 하락
- 랜덤 대비 유의미한 성능 유지 시 구조적 신뢰성 확보

---

## e3. w30 Window 제거

### 제외 컬럼
```python
# w30 aggregation
num_days_active_w30
total_secs_w30
avg_secs_per_day_w30
std_secs_w30
num_songs_w30
avg_songs_per_day_w30
num_unq_w30
num_25_w30
num_100_w30
short_play_w30
skip_ratio_w30
completion_ratio_w30
short_play_ratio_w30
variety_ratio_w30

# w30 dependent trends
secs_trend_w7_w30
secs_trend_w14_w30
days_trend_w7_w30
songs_trend_w7_w30
songs_trend_w14_w30
skip_trend_w7_w30
completion_trend_w7_w30
```

### 실험 목적
- 예측 시점에 가까운 정보 의존성 검증
- 집계 지연/누락 상황 가정

### 예상 결과
- 성능 점진적 감소
- 급격한 붕괴 없을 경우 중기 행동 패턴 학습 확인

---

## e3.1. w30 off + e2.1

### 제외 컬럼
```python
# w30
num_days_active_w30
total_secs_w30
avg_secs_per_day_w30
std_secs_w30
num_songs_w30
avg_songs_per_day_w30
num_unq_w30
num_25_w30
num_100_w30
short_play_w30
skip_ratio_w30
completion_ratio_w30
short_play_ratio_w30
variety_ratio_w30

secs_trend_w7_w30
secs_trend_w14_w30
days_trend_w7_w30
songs_trend_w7_w30
songs_trend_w14_w30
skip_trend_w7_w30
completion_trend_w7_w30

# transactions
days_since_last_payment
days_since_last_cancel
last_plan_days
total_payment_count
total_amount_paid
avg_amount_per_payment
unique_plan_count
subscription_months_est
payment_count_last_30d
payment_count_last_90d

# leakage risk
reg_days
is_auto_renew_last
```

### 실험 목적
- 운영 환경 최악 조건 가정
- 모델 일반화 성능 최종 검증

### 예상 결과
- 성능 최저
- 유지된다면 운영 배포 가능성 매우 높음

---

## 최종 요약 및 모델 선정 결과

본 실험(Feature Ablation)의 결과는 `model_selection_checklist.md`에 상세히 기록되었으며, 핵심 결론은 다음과 같다.

1.  **Robustness 검증:**
    *   **CatBoost**와 **MLP**는 핵심 Feature(결제 이력 등) 제거 시에도 성능이 완만하게 감소하며(Gradient Drop), 특정 정보에 과도하게 의존하지 않는 안정적인 학습 패턴을 입증했다.
    *   반면 **XGBoost**와 **RandomForest**는 정보 부재 시 성능이 급락하여(Cliff Drop) 운영 안전성 기준을 충족하지 못했다.

2.  **최종 결론:**
    *   실험 결과에 따라 **CatBoost**를 Primary Model로, **MLP**를 Secondary Candidate로 최종 선정한다.
    *   이는 단순히 최고 성능(Accuracy)이 아니라, 데이터 누락이나 환경 변화에도 견딜 수 있는 **Robustness**를 최우선 기준으로 삼은 결과이다.
