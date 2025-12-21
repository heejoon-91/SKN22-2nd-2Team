# Model Selection Checklist
*(Performance & Robustness focused)*

본 문서는 **추론 모델 선정**을 위해 사용되는 공식 기준 문서이다.  
모든 항목은 주관적 해석이 아닌 **측정 가능한 팩트**에 기반한다.

---

## 1. 모델 선정 체크리스트 (Performance & Robustness)

### A. 비교 공정성 (최소 전제 조건)
- [x] Train / Test 분할이 고정되어 있으며, 모든 모델 및 실험이 동일 분할을 사용한다
- [x] Feature-set 정의(e0 / e1 / e2 / e2.1 / e3 / e3.1)는 명확히 고정되어 있고, 실험 간 변경되는 요소는 feature 포함 여부뿐이다
- [x] 평가지표 산출 방식(ROC-AUC, PR-AUC, Recall 등)이 모든 실험에서 동일하다

---

### B. 선정 기준 및 임계값 정의 (Defined Thresholds)

**1. 최종 선정 지표:**
*   **Primary:** Recall (Churn 방어 목적)
*   **Secondary:** PR-AUC

**2. 수치적 판단 기준 (Numerical Thresholds):**
*   **급락 (Steep Drop):** ΔRecall ≥ 0.15 (Base 대비)
*   **운영 불가 수준 (Unusable):** Recall < 0.75 (Predictive Power 상실 간주)
*   **유의미한 차이 (Significant):** Metric 차이 > 0.02

---

### C. Robustness (Feature Ablation Stress Test)

#### Leakage / 상태성 의존성 (e0 → e1)
- [x] 성능 감소폭(ΔROC-AUC, ΔPR-AUC, ΔRecall)을 계산했다.
    - **CatBoost:** ΔRecall -0.0237 (Stable)
    - **MLP:** ΔRecall -0.0237 (Stable)
    - **LightGBM:** ΔRecall -0.0197 (Stable)
    - **XGBoost:** ΔRecall -0.0322 (Stable)
- [x] 성능 감소가 급격하지 않다 (모든 모델 통과).

#### 결제 정보 의존성 (e0 → e2)
- [x] e0 → e2(transactions off)에서 성능 감소폭을 계산했다.
    - **CatBoost:** Recall 0.93 -> 0.85 (**Pass**)
    - **MLP:** Recall 0.92 -> 0.85 (**Pass**)
    - **LightGBM:** Recall 0.90 -> 0.80 (**Pass**)
    - **XGBoost:** Recall 0.85 -> 0.63 (**FAIL**: < 0.75 & Δ > 0.15)
    - **RandomForest:** Recall 0.81 -> 0.62 (**FAIL**: < 0.75)
- [x] Logs-only 조건에서도 모델이 유의미한 예측력을 유지한다.
    - **통과 모델:** CatBoost, LightGBM, LogisticRegression, MLP

#### 최신 정보 의존성 (e0 → e3)
- [x] e0 → e3(w30 off)에서 성능 감소폭을 계산했다.
    - Most models showed similar trends to e2.
- [x] 최신 30일 집계 제거 시 성능이 붕괴하지 않는다.

#### 최악 조건 검증 (e3.1)
- [x] e3.1 조건에서의 성능을 기록했다.
    - **CatBoost:** Recall 0.8515
    - **MLP:** Recall 0.8489
    - **LightGBM:** Recall 0.8023
- [x] e3.1 성능이 베이스라인 모델보다 유의미하게 높다.

---

### D. 모델 선정 규칙
- [x] 최종 선정 지표 1~2개를 사전에 고정했다 (Recall, PR-AUC).
- [x] Robustness 결과(e3.1 성능 또는 감소폭)를 선정 판단에 반영한다.
- [x] 성능 최고 모델이 아닌 경우에도, Robustness가 현저히 우수하면 우선 후보로 고려한다.

---

## 2. 모델 탈락 기준표 (Fail-Fast Rules) - 적용 결과

아래 조건 중 **하나라도 충족되면 해당 모델은 추론 모델 후보에서 탈락**한다.

| 구분 | 탈락 조건 (팩트 기준) | 적용 결과 (Disqualified Models) |
|---|---|---|
| 누수/상태성 의존 | e1에서 성능 급락 (ΔRecall ≥ 0.15) | 없음 |
| 결제 의존 | e2에서 성능이 운영 불가 수준으로 붕괴 (Recall < 0.75) | **XGBoost (0.63), RandomForest (0.62)** |
| 최신 정보 의존 | e3에서 성능이 급락 | **XGBoost, RandomForest** |
| 최악 조건 실패 | e3.1에서 베이스라인보다 유의미하게 못함 | - |
| 일반화 실패 | Validation 대비 Test 성능이 반복적으로 현저히 낮음 | - |
| 불안정성 | 동일 조건 반복 학습 시 지표 변동 폭이 큼 | - |
| KPI 미달 | Test 기준 목표 KPI 미달 | **LogisticRegression** (Baseline PR-AUC 낮음) |

**Survivors:** CatBoost, LightGBM, MLP

---

## 3. 최종 선정 및 결론

### 비교 (Survivors)
*   **CatBoost:** e3.1 Recall **0.85** (Very Robust), PR-AUC 0.79
*   **MLP:** e3.1 Recall **0.85** (Very Robust), PR-AUC 0.79
*   **LightGBM:** e3.1 Recall **0.80**, PR-AUC 0.79

### Recommendation
**최종 선정 모델: CatBoost (Primary), MLP (Secondary Candidate)**

**근거:**
1.  **Superior Robustness:** CatBoost와 MLP 모두 결제 정보 부재(e2) 및 최악 조건(e3.1)에서 Recall 0.85 수준을 유지하며 매우 뛰어난 안정성을 입증함. (LightGBM 0.80 대비 우수)
2.  **Fail-Fast 통과:** XGBoost, RF가 붕괴한 구간에서도 두 모델은 안정적임.
3.  **결론:** Tabular 데이터 특성상 학습/추론 속도와 운영 편의성을 고려하여 **CatBoost**를 1순위로 선정하되, 딥러닝 파이프라인이 필요할 경우 **MLP**도 동등한 성능의 대안으로 확보함.

---

## 4. 한 줄 결론

> Feature Ablation 실험을 통과하지 못하는 모델(XGBoost, RF)은 제외되었으며,  
> **CatBoost**와 **MLP**가 가장 높은 Robustness(e3.1 Recall 0.85)를 보여 최종 후보로 선정됨.
