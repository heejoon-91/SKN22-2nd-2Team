# e0. 전체 컬럼

```python
RANDOM_STATE = 719

ID_COL = "msno"
TARGET_COL = "is_churn"

CATEGORICAL_COLS = [
    "city", "gender", "registered_via", "last_payment_method",
    "has_ever_paid", "has_ever_cancelled",
    "is_auto_renew_last",
    "is_free_user",
]

NUMERICAL_COLS = [
    "reg_days",

    # ======================
    # w7
    # ======================
    "num_days_active_w7", "total_secs_w7", "avg_secs_per_day_w7", "std_secs_w7",
    "num_songs_w7", "avg_songs_per_day_w7", "num_unq_w7", "num_25_w7", "num_100_w7",
    "short_play_w7", "skip_ratio_w7", "completion_ratio_w7", "short_play_ratio_w7", "variety_ratio_w7",

    # ======================
    # w14
    # ======================
    "num_days_active_w14", "total_secs_w14", "avg_secs_per_day_w14", "std_secs_w14",
    "num_songs_w14", "avg_songs_per_day_w14", "num_unq_w14", "num_25_w14", "num_100_w14",
    "short_play_w14", "skip_ratio_w14", "completion_ratio_w14", "short_play_ratio_w14", "variety_ratio_w14",

    # ======================
    # w21
    # ======================
    "num_days_active_w21", "total_secs_w21", "avg_secs_per_day_w21", "std_secs_w21",
    "num_songs_w21", "avg_songs_per_day_w21", "num_unq_w21", "num_25_w21", "num_100_w21",
    "short_play_w21", "skip_ratio_w21", "completion_ratio_w21", "short_play_ratio_w21", "variety_ratio_w21",

    # ======================
    # w30  (OFF → 주석 처리)
    # ======================
    "num_days_active_w30", "total_secs_w30", "avg_secs_per_day_w30", "std_secs_w30",
    "num_songs_w30", "avg_songs_per_day_w30", "num_unq_w30", "num_25_w30", "num_100_w30",
    "short_play_w30", "skip_ratio_w30", "completion_ratio_w30", "short_play_ratio_w30", "variety_ratio_w30",

    # ======================
    # trend (주의: 상위 window에 종속됨)
    # ======================
    # w7–w14
    "days_trend_w7_w14",

    # w7–w30 / w14–w30 (w30 OFF 시 같이 OFF)
    "secs_trend_w7_w30", "secs_trend_w14_w30",
    "days_trend_w7_w30",
    "songs_trend_w7_w30", "songs_trend_w14_w30",
    "skip_trend_w7_w30", "completion_trend_w7_w30",

    # ======================
    # transactions (logs-only 실험 시 OFF)
    # ======================
    "days_since_last_payment", "days_since_last_cancel", "last_plan_days",
    "total_payment_count", "total_amount_paid", "avg_amount_per_payment",
    "unique_plan_count", "subscription_months_est",
    "payment_count_last_30d", "payment_count_last_90d",
]

FEATURE_COLS = CATEGORICAL_COLS + NUMERICAL_COLS

X = df[FEATURE_COLS].copy()
y = df[TARGET_COL].astype(int).copy()
```

---

# e1. 조건부 leakage 위험 예상 컬럼 off
- 제외할 컬럼 :
    > `days_since_last_payment`
    > `days_since_last_cancel`
    > `reg_days`
    > `is_auto_renew_last`

---

# e2. Transactions 컬럼 off
- 제외할 컬럼: Transactions 파생 집계 컬럼

---

# e2.1. Transactions 컬럼 off + e1
- 제외할 컬럼: e2 + e1

---

# e3. w30 Off
- 제외할 컬럼: 
    > `num_days_active_w30`, `total_secs_w30`, `avg_secs_per_day_w30`, `std_secs_w30`,
    > `num_songs_w30`, `avg_songs_per_day_w30`, `num_unq_w30`, `num_25_w30`, `num_100_w30`,
    > `short_play_w30`, `skip_ratio_w30`, `completion_ratio_w30`, `short_play_ratio_w30`, `variety_ratio_w30`,

    > `secs_trend_w7_w30`, `secs_trend_w14_w30`,
    > `days_trend_w7_w30`,
    > `songs_trend_w7_w30`, `songs_trend_w14_w30`,
    > `skip_trend_w7_w30`, `completion_trend_w7_w30`,

# e3.1. w30 off + e2.1.
- 제외할 컬럼: 