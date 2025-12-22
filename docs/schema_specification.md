
# 모델 스키마 명세서 (Model Schema Specification)

이 문서는 KKBox 이탈 예측 시스템의 두 가지 핵심 모델(V4, V5.2)에서 사용되는 입력 변수(Feature)의 계산 로직과 정의를 기술합니다.

## 모델 개요 (Models Overview)
*   **V4 (Track 1: Main)**: **이력 + 행동 + 상태(Status)**를 모두 활용. 정밀 예측 및 타겟팅 용도.
*   **V5.2 (Track 2: Behavior)**: **이력 + 행동 + 추세(Trend)**를 활용하며, **상태(Status) 변수는 제외**. 조기 경보 및 잠재 이탈 탐지 용도.

---

## 1. 공통 사용 변수 (Common Features: V4 & V5.2)
**V4**와 **V5.2** 모델 모두에서 핵심적으로 사용되는 변수들입니다.

### A. 전략적 파생 변수 (Strategic Derived Features)
비즈니스 인사이트를 도출하기 위해 특별히 설계된 고차원 변수입니다.

| 변수명 (Feature) | 계산식 (Formula Logic) | 비즈니스 의미 |
| :--- | :--- | :--- |
| **active_decay_rate** | `num_days_active_w7 / (num_days_active_w30 / 4)` | **활동 감소율**. 평소(30일) 대비 최근(7일) 활동량이 얼마나 줄었는지 측정 (1.0 미만 시 감소). |
| **listening_time_velocity** | `avg_secs_per_day_w7 - avg_secs_per_day_w14` | **청취 가속도**. 최근 2주간 청취 시간이 증가세인지 감소세인지 측정 (음수면 급감). |
| **discovery_index** | `num_unq_w7 / num_songs_w7` | **탐색 지수**. 반복 청취 대비 새로운 곡을 얼마나 듣는지 측정 (1에 가까울수록 탐색형). |
| **skip_passion_index** | `num_25_w7 / num_100_w7` | **스킵 열정도**. 완청 곡 대비 스킵 곡의 비율 (높을수록 불만족/탐색 높음). |
| **engagement_density** | `total_secs_w7 / num_days_active_w7` | **활동 밀도**. 접속 시 평균적으로 얼마나 오래 체류하는지 측정. |
| **last_active_gap** | `Target Date - Last User Log Date` | **마지막 활동 경과일**. 구독 중임에도 접속하지 않은 잠수 기간. |

### B. 사용자 프로필 및 이력 (Profile & History)
사용자의 고정적인 속성 및 과거 결제 맥락 정보입니다.

| 변수명 (Feature) | 계산식/출처 | 설명 |
| :--- | :--- | :--- |
| **bd_clean** | `Age` (전처리: 이상치 제거) | 사용자 나이. |
| **reg_days** | `Target Date - Registration Date` | 가입 후 경과 일수 (서비스 이용 기간). |
| **city**, **gender** | Raw Data | 거주 도시 및 성별. |
| **registered_via** | Raw Data | 가입 경로 코드. |
| **subscription_months_est** | `reg_days / 30.0` | 예상 구독 유지 개월 수 (충성도 정보). |
| **avg_amount_per_payment** | `Total Amount / Total Tx Count` | 1회 평균 결제 금액 (ARPPU 관련). |
| **unique_plan_count** | `CountDistinct(Plan ID)` | 과거에 이용해본 요금제 종류 수. |
| **has_ever_cancelled** | `Cancel Count > 0` | 해지 경험 유무 (습관적 이탈 가능성). |

### C. 기본 청취 행동 (Basic Behavior)
최근 활동 기록의 단순 집계입니다. (*`_w*` 접미사는 w7, w14, w21, w30 주기를 의미*)

| 변수명 (Feature) | 계산식 (Formula Logic) | 설명 |
| :--- | :--- | :--- |
| **num_days_active_w*** | `CountDistinct(Log Date)` | 기간 내 접속 일수. |
| **total_secs_w*** | `Sum(Total Seconds)` | 기간 내 총 청취 시간. |
| **num_songs_w*** | `Sum(Num Unq + Num 100...)` | 기간 내 총 청취 곡 수. |
| **num_unq_w*** | `Sum(Num Unq)` | 기간 내 청취한 고유 곡 수. |
| **completion_ratio_w*** | `num_100_w* / num_songs_w*` | 곡 완청률. |

---

## 2. V5.2 전용 변수 (V5.2 Exclusive: Trends & Variance)
**V5.2 모델**은 상태(Status) 정보를 볼 수 없으므로, 미세한 행동 변화를 감지하기 위해 **추세(Trend) 변수**를 추가로 사용합니다.

| 변수명 (Feature) | 계산식 (Formula Logic) | 설명 |
| :--- | :--- | :--- |
| **secs_trend_w7_w30** | `avg_secs_w7 - avg_secs_w30` (Normalized) | **청취 시간 변화량**. 장기(30일) 대비 단기(7일) 변화. |
| **days_trend_w7_w30** | `avg_days_w7 - avg_days_w30` (Normalized) | **접속 빈도 변화량**. |
| **skip_trend_w7_w30** | `skip_ratio_w7 - skip_ratio_w30` | **스킵 성향 변화량**. 최근에 스킵이 더 늘었는지 확인. |
| **daily_listening_variance** | `StdDev(Daily Seconds w7)` | **청취 패턴 불규칙성**. 값이 클수록 불규칙한 사용 패턴. |

---

## 3. V4 전용 변수 (V4 Exclusive: Payment Status)
**V4 모델**은 **현재 결제 상태**를 직접적으로 확인하여 이탈 임박 여부를 판별합니다. **V5.2에서는 제외**됩니다.

| 변수명 (Feature) | 계산식 (Formula Logic) | 설명 |
| :--- | :--- | :--- |
| **days_since_last_payment** | `Target Date - Last Payment Date` | **결제 공백기**. 가장 강력한 이탈 예측 변수 (갱신 안 됨). |
| **is_auto_renew_last** | `Last Tx Auto Renew?` | **자동 갱신 여부**. 해제 시 이탈 확률 급상승. |
| **is_free_user** | `No Payment History` | **무료 유저 여부**. |
| **days_since_last_cancel** | `Target Date - Last Cancel` | **최근 해지 경과일**. 최근에 해지 이력이 있는지. |
| **payment_count_last_30d** | `Count(Tx) in [T-30, T]` | 최근 30일 간의 결제 시도 횟수. |
