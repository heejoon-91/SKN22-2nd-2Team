
# 모델 스키마 명세서 (Model Schema Specification)

이 문서는 KKBox 이탈 예측 시스템의 두 가지 핵심 모델에서 사용되는 입력 변수(Feature)를 정의합니다.

## 모델 개요 (Models Overview)

*   **V4 (Track 1: 메인 모델)**: 사용자 행동, 결제 이력, 그리고 **현재 결제 상태**를 모두 통합한 종합 모델입니다. 즉각적인 이탈 위험을 감지하는 "응급실(Emergency Room)" 역할을 수행합니다.
*   **V5.2 (Track 2.5: 안심 행동 모델)**: 행동 및 결제 **이력**에 집중하며, 현재 결제 상태 지표는 의도적으로 **제외**한 모델입니다. 금전적 이탈이 발생하기 전 행동적 철수(Withdrawal) 징후를 감지하는 "건강검진(Check-up)" 역할을 수행합니다.

---

## 1. 변수 카테고리 (Feature Categories)

### A. 사용자 프로필 (User Profile - 공통)
사용자의 고정적인 속성 정보입니다.
*   `city`: 거주 도시 코드 (범주형)
*   `gender`: 성별 (범주형)
*   `registered_via`: 가입 경로 코드 (범주형)
*   `reg_days`: 가입 후 경과 일수 (수치형)

### B. 결제 이력 및 환경 (Payment History & Context - 공통)
사용자의 소비 습관과 충성도를 나타내는 과거 결제 패턴입니다.
*   `subscription_months_est`: 예상 구독 유지 기간 (충성도 지표)
*   `total_payment_count`: 총 결제 횟수
*   `total_amount_paid`: 총 누적 결제 금액
*   `avg_amount_per_payment`: 1회 평균 결제 금액
*   `unique_plan_count`: 이용해본 요금제 종류 수
*   `last_payment_method`: 마지막으로 사용한 결제 수단 코드 (범주형)
*   `has_ever_paid`: 과거 결제 이력 유무 (범주형)
*   `has_ever_cancelled`: 과거 해지 이력 유무 (범주형)
*   `is_free_user`: 현재 무료 사용자 여부 (범주형)

### C. 청취 행동 (Listening Behavior - 공통)
다양한 기간(최근 7일/14일/21일/30일) 동안 집계된 활동 지표입니다.
*참고: V4는 주로 w7/w14/w21을 사용하고, V5.2는 w7/w14/w21/w30 및 추세(Trend) 변수까지 폭넓게 사용합니다.*

**핵심 지표 (Core Metrics - w7/w14/w21/w30)**:
*   `num_days_active_w*`: 해당 기간 동안의 접속 일수
*   `total_secs_w*`: 총 청취 시간 (초)
*   `num_unq_w*`: 청취한 고유 곡 수
*   `num_songs_w*`: 총 청취 곡 수
*   `avg_secs_per_day_w*`: 일평균 청취 시간
*   `avg_songs_per_day_w*`: 일평균 청취 곡 수

**파생 비율 (Derived Ratios - w7/w14/w21/w30)**:
*   `completion_ratio_w*`: 곡 완청률 (100% 재생 비율)
*   `skip_ratio_w*`: 곡 스킵 비율 (중간에 넘김)
*   `short_play_ratio_w*`: 25% 미만 짧은 청취 비율
*   `variety_ratio_w*`: 청취 다양성 비율 (고유 곡 수 / 총 곡 수)
*   `daily_listening_variance`: (V5.2) 일별 청취 시간의 불규칙성(분산)

**추세 변수 (Trend Features - V5.2 전용)**:
*   `secs_trend_w7_w30`: 단기(7일) 대비 장기(30일) 청취 시간 변화 추세
*   `days_trend_w7_w30`: 접속 빈도 변화 추세
*   `skip_trend_w7_w30`: 스킵 행동의 변화 추세

### D. 결제 상태 (Payment Status - V4 전용)
**중요**: 이 변수들은 **V5.2에서 엄격히 제외**됩니다. 이는 V5.2가 결제 상태가 아닌 행동 변화만을 감지하도록 강제하기 위함입니다.
*   `days_since_last_payment`: 마지막 결제일로부터 경과한 일수
*   `days_since_last_cancel`: 마지막 해지일로부터 경과한 일수 (최근 이력 없으면 0)
*   `is_auto_renew_last`: 마지막 결제가 자동 갱신이었는지 여부
*   `payment_count_last_30d`: 최근 30일 내 결제 성공 횟수
*   `payment_count_last_90d`: 최근 90일 내 결제 성공 횟수
*   `last_plan_days`: 마지막으로 구매한 이용권의 기간(일수)

### E. 파생 행동 지표 (Derived Behavioral Scores)
예측력을 높이기 위해 정교하게 설계된 파생 변수들입니다.

| 변수명 | 설명 | 계산식 (Formula) | 비고 |
| :--- | :--- | :--- | :--- |
| **active_decay_rate** | 활동 감소율 | `num_days_active_w7` ÷ (`num_days_active_w30` ÷ 4) | 1.0 미만이면 최근 활동이 평균(지난 30일)보다 감소함. |
| **listening_time_velocity** | 청취 시간 변화 속도 | `avg_secs_per_day_w7` - `avg_secs_per_day_w14` | (+)면 증가 추세, (-)면 감소 추세. |
| **discovery_index** | 새로운 곡 탐색 지수 | `num_unq_w7` ÷ `num_songs_w7` | 1에 가까울수록 매번 새로운 곡을 듣는 성향(탐색형). |
| **skip_passion_index** | 스킵 대비 완청 지수 | `num_25_w7` (Short) ÷ `num_100_w7` (Complete) | 값이 클수록 스킵을 많이 하고 완청을 안 함 (부정적 청취). |
| **engagement_density** | 활동 밀도 | `total_secs_w7` ÷ `num_days_active_w7` | 하루 접속 시 평균적으로 얼마나 오래 듣는가. |

---

## 2. 모델별 변수 비교표 (Comparison Matrix)

| 변수 그룹 (Feature Group) | V4 (Track 1: 메인) | V5.2 (Track 2.5: 안심 행동) |
| :--- | :---: | :---: |
| **사용자 프로필 (Profile)** | ✅ | ✅ |
| **결제 이력/환경 (Context)** | ✅ | ✅ |
| **청취 행동 (Behavior)** | ✅ | ✅ (추세 변수 포함 강화) |
| **파생 행동 지표 (Scores)** | ✅ | ✅ |
| **결제 상태 (Status)** | ✅ | ❌ **제외 (Excluded)** |
