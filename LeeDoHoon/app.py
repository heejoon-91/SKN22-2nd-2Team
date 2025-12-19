# -*- coding: utf-8 -*-
"""
KKBox Churn Prediction Dashboard
================================
작성자: 이도훈 (LDH)
작성일: 2025-12-17

Streamlit 기반 이탈 예측 대시보드
"""

import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="KKBox Churn Prediction",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링 - 라이트 테마
st.markdown("""
<style>
    /* 전체 폰트 및 배경 */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    code, .stCode {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* 메인 배경 - 밝은 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
    }
    
    /* 사이드바 스타일 - 밝은 배경 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #334155;
        font-weight: 500;
    }
    
    /* 메트릭 카드 */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        color: #059669;
    }
    
    /* 컨테이너 스타일 */
    .main-header {
        background: linear-gradient(90deg, #dbeafe, #e0e7ff);
        border: 1px solid #93c5fd;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .info-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* 테이블 스타일 */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #6366f1);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #1e40af;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* 프로그레스 바 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    }
    
    /* 플레이스홀더 카드 */
    .placeholder-card {
        background: #fffbeb;
        border: 2px dashed #f59e0b;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
    }
    
    .placeholder-card h3 {
        color: #b45309;
        margin-bottom: 1rem;
    }
    
    /* 성능 지표 배지 */
    .metric-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .metric-badge.excellent {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
    }
    
    .metric-badge.good {
        background: #dbeafe;
        color: #1e40af;
        border: 1px solid #93c5fd;
    }
    
    /* 헤더 텍스트 - 어두운 색 */
    h1, h2, h3, h4 {
        color: #1e293b !important;
    }
    
    p, li, span {
        color: #334155;
    }
    
    /* 일반 텍스트 */
    .stMarkdown {
        color: #334155;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        color: #1e293b;
    }
    
    /* 입력 필드 */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        color: #1e293b;
    }
    
    /* JSON 표시 */
    .stJson {
        background: #f8fafc;
    }
    
    /* 경고/정보 박스 */
    .stAlert {
        background: #f0f9ff;
        color: #0c4a6e;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # 사이드바 네비게이션
    with st.sidebar:
        st.markdown("# 🎵 KKBox")
        st.markdown("### Churn Prediction")
        st.markdown("---")
        
        page = st.radio(
            "📍 Navigation",
            [
                "🏠 Home",
                "📊 데이터 탐색 (EDA)",
                "🤖 ML 모델 결과",
                "🧠 DL 모델 결과",
                "⚖️ 모델 비교",
                "📌 BM 전략 / 세그먼트",
                "🎯 추론 (Inference)",
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; font-size: 0.85rem;'>
            <p style='color: #64748b;'>👤 작성자: 이도훈 (LDH)</p>
            <p style='color: #64748b;'>📅 2025-12-17</p>
        </div>
        """, unsafe_allow_html=True)

    # 페이지 라우팅
    if page == "🏠 Home":
        show_home()
    elif page == "📊 데이터 탐색 (EDA)":
        show_eda()
    elif page == "🤖 ML 모델 결과":
        show_ml_results()
    elif page == "🧠 DL 모델 결과":
        show_dl_results()
    elif page == "⚖️ 모델 비교":
        show_model_comparison()
    elif page == "📌 BM 전략 / 세그먼트":
        show_bm_strategy()
    elif page == "🎯 추론 (Inference)":
        show_inference()


def show_home():
    """홈 페이지"""
    st.markdown("""
    <div class="main-header">
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem; color: #1e3a8a;'>
            🎵 KKBox Churn Prediction
        </h1>
        <p style='font-size: 1.2rem; color: #475569;'>
            머신러닝 & 딥러닝 기반 고객 이탈 예측 시스템
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 프로젝트 개요
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3 style='color: #1e40af;'>🎯 프로젝트 목표</h3>
            <p style='color: #334155;'>이탈 가능성이 높은 고객을 사전에 식별하여 선제적 대응 전략 수립</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3 style='color: #1e40af;'>📊 문제 유형</h3>
            <p style='color: #334155;'>이진 분류 (Binary Classification)<br/>
            타겟: is_churn (1=이탈, 0=유지)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3 style='color: #1e40af;'>⏰ 예측 프레임</h3>
            <p style='color: #334155;'>관측 윈도우: 2017-03-01 ~ 03-31<br/>
            예측 시점(T): 2017-04-01</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 데이터셋 정보
    st.markdown("### 📁 데이터셋 구성")
    
    data_info = {
        "테이블": ["train_v2.csv", "user_logs_v2.csv", "transactions.csv", "members_v3.csv"],
        "설명": ["사용자별 이탈 라벨", "일별 음악 청취 로그", "결제/구독 거래 내역", "사용자 기본 정보"],
        "용도": ["타겟 변수 (Y)", "행동 Feature 생성", "결제 Feature 생성", "정적 Feature"]
    }
    
    import pandas as pd
    st.dataframe(pd.DataFrame(data_info), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 프로젝트 진행 상황
    st.markdown("### 📈 프로젝트 진행 현황")
    
    progress_data = [
        ("✅ 문제 정의 및 예측 프레임 설정", 100),
        ("✅ 데이터 전처리 및 Feature Engineering", 100),
        ("✅ ML 모델 학습 (Logistic Regression, LightGBM)", 100),
        ("🔄 DL 모델 학습 (MLP)", 0),
        ("✅ 최적 모델 선정 및 저장 (LightGBM)", 100),
        ("✅ BM 전략 및 Inference UI 구축", 100),
    ]
    
    for task, progress in progress_data:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{task}**")
            st.progress(progress / 100)
        with col2:
            if progress == 100:
                st.markdown(f"<span style='color: #059669; font-weight: bold;'>{progress}%</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #d97706; font-weight: bold;'>{progress}%</span>", unsafe_allow_html=True)


def show_eda():
    """데이터 탐색 페이지"""
    import pandas as pd
    import json
    import os
    
    st.markdown("## 📊 데이터 탐색 (EDA)")
    
    tab1, tab2, tab3 = st.tabs(["📋 Feature 목록", "📈 데이터 통계", "🎯 클래스 분포"])
    
    with tab1:
        st.markdown("### 학습에 사용된 Feature (35개)")
        
        # Feature 목록 로드
        try:
            with open("models/feature_cols.json", "r") as f:
                features = json.load(f)
            
            # 카테고리별 분류
            user_log_features = [f for f in features if any(x in f for x in ['songs', 'secs', 'num_', 'skip', 'complete', 'partial', 'listening', 'avg_song'])]
            transaction_features = [f for f in features if any(x in f for x in ['payment', 'cancel', 'auto_renew', 'discount', 'transaction', 'plan', 'expire'])]
            member_features = [f for f in features if any(x in f for x in ['city', 'age', 'registered', 'tenure', 'gender'])]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 🎧 청취 행동 Feature")
                for f in user_log_features:
                    st.markdown(f"- `{f}`")
                    
            with col2:
                st.markdown("#### 💳 결제 Feature")
                for f in transaction_features:
                    st.markdown(f"- `{f}`")
                    
            with col3:
                st.markdown("#### 👤 회원 정보 Feature")
                for f in member_features:
                    st.markdown(f"- `{f}`")
                    
        except FileNotFoundError:
            st.warning("Feature 목록 파일을 찾을 수 없습니다.")
    
    with tab2:
        st.markdown("### 주요 피처 통계 (30일 윈도우 기준)")
        
        stats_data = {
            "피처": ["num_days_active_w30", "total_secs_w30", "num_songs_w30", "skip_ratio_w30", "completion_ratio_w30"],
            "Mean": ["16.66", "131,733", "642", "0.20", "0.80"],
            "Std": ["10.30", "185,227", "829", "0.18", "0.18"],
            "Min": ["1", "0.3", "1", "0", "0"],
            "25%": ["7", "13,115", "73", "0.06", "0.71"],
            "50%": ["18", "67,936", "354", "0.15", "0.85"],
            "75%": ["26", "173,934", "877", "0.29", "0.94"],
            "Max": ["31", "2,406,313", "11,490", "1.0", "1.0"]
        }
        
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)
        
        st.markdown("### 추세 피처 통계")
        
        trend_data = {
            "피처": ["secs_trend_w7_w30", "recency_secs_ratio", "skip_trend_w7_w30", "completion_trend_w7_w30"],
            "Mean": ["0.23", "0.23", "-0.05", "-0.10"],
            "Std": ["0.22", "0.22", "0.19", "0.28"],
            "해석": ["평균적으로 최근 7일이 전체의 23%", "동일 (7/30 ≈ 23%)", "평균적으로 스킵율 5%p 감소", "평균적으로 완주율 10%p 감소"]
        }
        
        st.dataframe(pd.DataFrame(trend_data), use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 클래스 분포 (Train Set)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 클래스 분포 시각화
            import plotly.express as px
            
            class_dist = pd.DataFrame({
                'Class': ['Retention (0)', 'Churn (1)'],
                'Count': [618541, 61131],
                'Percentage': [91.0, 9.0]
            })
            
            fig = px.pie(
                class_dist, 
                values='Count', 
                names='Class',
                color_discrete_sequence=['#3b82f6', '#ef4444'],
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_color='white')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1e293b'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("""
            <div class="info-card">
                <h4 style='color: #1e40af;'>📊 클래스 불균형 현황</h4>
                <ul style='color: #334155;'>
                    <li><strong>유지 (Retention)</strong>: 618,541명 (91%)</li>
                    <li><strong>이탈 (Churn)</strong>: 61,131명 (9%)</li>
                </ul>
                <h4 style='color: #1e40af;'>⚖️ 불균형 처리 방법</h4>
                <ul style='color: #334155;'>
                    <li>Logistic Regression: class_weight='balanced'</li>
                    <li>LightGBM: scale_pos_weight ≈ 10.1</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)


def show_ml_results():
    """ML 모델 결과 페이지"""
    import pandas as pd
    import json
    import plotly.express as px
    import plotly.graph_objects as go
    
    st.markdown("## 🤖 ML 모델 학습 결과")
    
    # 결과 로드
    try:
        with open("models/training_results.json", "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        st.error("학습 결과 파일을 찾을 수 없습니다.")
        return
    
    tab1, tab2, tab3 = st.tabs(["📊 성능 비교", "📈 Feature Importance", "🔧 하이퍼파라미터"])
    
    with tab1:
        st.markdown("### Test Set 성능 비교")
        
        # 메트릭 카드
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔹 Logistic Regression (Baseline)")
            lr_test = results["Logistic Regression"]["test_metrics"]
            
            m1, m2, m3 = st.columns(3)
            m1.metric("ROC-AUC", f"{lr_test['roc_auc']:.4f}")
            m2.metric("PR-AUC", f"{lr_test['pr_auc']:.4f}")
            m3.metric("Recall", f"{lr_test['recall']:.4f}")
            
            m4, m5, m6 = st.columns(3)
            m4.metric("Precision", f"{lr_test['precision']:.4f}")
            m5.metric("F1-Score", f"{lr_test['f1']:.4f}")
            m6.metric("Specificity", f"{lr_test['specificity']:.4f}")
            
        with col2:
            st.markdown("#### 🔸 LightGBM")
            lgb_test = results["LightGBM"]["test_metrics"]
            
            m1, m2, m3 = st.columns(3)
            m1.metric("ROC-AUC", f"{lgb_test['roc_auc']:.4f}", f"+{(lgb_test['roc_auc'] - lr_test['roc_auc']):.4f}")
            m2.metric("PR-AUC", f"{lgb_test['pr_auc']:.4f}", f"+{(lgb_test['pr_auc'] - lr_test['pr_auc']):.4f}")
            m3.metric("Recall", f"{lgb_test['recall']:.4f}", f"+{(lgb_test['recall'] - lr_test['recall']):.4f}")
            
            m4, m5, m6 = st.columns(3)
            m4.metric("Precision", f"{lgb_test['precision']:.4f}", f"+{(lgb_test['precision'] - lr_test['precision']):.4f}")
            m5.metric("F1-Score", f"{lgb_test['f1']:.4f}", f"+{(lgb_test['f1'] - lr_test['f1']):.4f}")
            m6.metric("Specificity", f"{lgb_test['specificity']:.4f}", f"+{(lgb_test['specificity'] - lr_test['specificity']):.4f}")
        
        st.markdown("---")
        
        # 바 차트 비교
        st.markdown("### 지표별 비교 시각화")
        
        metrics = ['ROC-AUC', 'PR-AUC', 'Recall', 'Precision', 'F1-Score']
        lr_values = [lr_test['roc_auc'], lr_test['pr_auc'], lr_test['recall'], lr_test['precision'], lr_test['f1']]
        lgb_values = [lgb_test['roc_auc'], lgb_test['pr_auc'], lgb_test['recall'], lgb_test['precision'], lgb_test['f1']]
        
        fig = go.Figure(data=[
            go.Bar(name='Logistic Regression', x=metrics, y=lr_values, marker_color='#3b82f6'),
            go.Bar(name='LightGBM', x=metrics, y=lgb_values, marker_color='#8b5cf6')
        ])
        
        fig.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            yaxis=dict(gridcolor='rgba(100, 116, 139, 0.2)', range=[0, 1]),
            xaxis=dict(gridcolor='rgba(100, 116, 139, 0.2)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Confusion Matrix
        st.markdown("### Confusion Matrix (Test Set)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Logistic Regression")
            cm_lr = [
                [lr_test['true_negative'], lr_test['false_positive']],
                [lr_test['false_negative'], lr_test['true_positive']]
            ]
            
            fig_lr = px.imshow(
                cm_lr,
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=['Retention', 'Churn'],
                y=['Retention', 'Churn'],
                color_continuous_scale='Blues',
                text_auto=True
            )
            fig_lr.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1e293b')
            )
            st.plotly_chart(fig_lr, use_container_width=True)
            
        with col2:
            st.markdown("#### LightGBM")
            cm_lgb = [
                [lgb_test['true_negative'], lgb_test['false_positive']],
                [lgb_test['false_negative'], lgb_test['true_positive']]
            ]
            
            fig_lgb = px.imshow(
                cm_lgb,
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=['Retention', 'Churn'],
                y=['Retention', 'Churn'],
                color_continuous_scale='Purples',
                text_auto=True
            )
            fig_lgb.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#1e293b')
            )
            st.plotly_chart(fig_lgb, use_container_width=True)
    
    with tab2:
        st.markdown("### LightGBM Feature Importance (Top 15)")
        
        fi = results["LightGBM"]["feature_importance"][:15]
        fi_df = pd.DataFrame(fi)
        
        fig = px.bar(
            fi_df,
            x='importance',
            y='feature',
            orientation='h',
            color='importance',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e293b'),
            yaxis=dict(autorange='reversed', gridcolor='rgba(100, 116, 139, 0.2)'),
            xaxis=dict(gridcolor='rgba(100, 116, 139, 0.2)'),
            showlegend=False,
            coloraxis_showscale=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="info-card">
            <h4 style='color: #1e40af;'>🔍 주요 인사이트</h4>
            <ol style='color: #334155;'>
                <li><strong>days_to_expire</strong>: 만료까지 남은 일수가 가장 중요한 이탈 신호</li>
                <li><strong>auto_renew_rate</strong>: 자동 갱신 비율 - 낮을수록 이탈 위험</li>
                <li><strong>total_payment</strong>: 총 결제액 - 높은 LTV 고객 식별</li>
                <li><strong>cancel_count</strong>: 취소 횟수 - 불만족 신호</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 모델 하이퍼파라미터")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Logistic Regression")
            lr_params = results["Logistic Regression"]["params"]
            st.json(lr_params)
            
        with col2:
            st.markdown("#### LightGBM")
            lgb_params = results["LightGBM"]["params"]
            st.json(lgb_params)
            
            st.info(f"🏆 Best Iteration: {results['LightGBM']['best_iteration']}")

    # --- CatBoost (Recall 최적화) 별도 섹션 ---
    st.markdown("---")
    st.markdown("### 🟣 CatBoost (Recall 최적화) 결과")
    
    try:
        with open("models/recall_selected_results.json", "r") as f:
            cb = json.load(f)
    except FileNotFoundError:
        st.info("`recall_selected_results.json` 파일을 찾을 수 없어 CatBoost 결과를 표시할 수 없습니다.")
        return
    
    cb_test = cb["test_metrics_optimal"]
    cb_valid = cb["valid_metrics_optimal"]
    thr = cb["optimal_threshold"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Test Set (threshold 최적화)")
        m1, m2, m3 = st.columns(3)
        m1.metric("ROC-AUC", f"{cb_test['roc_auc']:.4f}")
        m2.metric("PR-AUC", f"{cb_test['pr_auc']:.4f}")
        m3.metric("Recall", f"{cb_test['recall']:.4f}")
        
        m4, m5, m6 = st.columns(3)
        m4.metric("Precision", f"{cb_test['precision']:.4f}")
        m5.metric("F1-Score", f"{cb_test['f1']:.4f}")
        m6.metric("Specificity", f"{cb_test['specificity']:.4f}")
        
        st.markdown(f"- 사용 threshold: **{thr:.3f}** (Validation Recall 기준 최적화)")
    
    with col2:
        st.markdown("#### Validation / Test Confusion Matrix (요약)")
        st.markdown(
            f"- Valid: TN={cb_valid['true_negative']:,}, FP={cb_valid['false_positive']:,}, "
            f"FN={cb_valid['false_negative']:,}, TP={cb_valid['true_positive']:,}"
        )
        st.markdown(
            f"- Test: TN={cb_test['true_negative']:,}, FP={cb_test['false_positive']:,}, "
            f"FN={cb_test['false_negative']:,}, TP={cb_test['true_positive']:,}"
        )
    
    # Feature Importance (Top 10)
    fi_cb = cb["feature_importance"][:10]
    fi_cb_df = pd.DataFrame(fi_cb)
    
    st.markdown("#### CatBoost Feature Importance (Top 10)")
    fig_cb = px.bar(
        fi_cb_df.sort_values("importance", ascending=True),
        x="importance",
        y="feature",
        orientation="h",
        color="importance",
        color_continuous_scale="Purples",
    )
    fig_cb.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#1e293b"),
        yaxis=dict(autorange="reversed", gridcolor="rgba(100, 116, 139, 0.2)"),
        xaxis=dict(gridcolor="rgba(100, 116, 139, 0.2)"),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_cb, use_container_width=True)


def show_dl_results():
    """DL 모델 결과 페이지 (Placeholder)"""
    st.markdown("## 🧠 DL 모델 학습 결과")
    
    st.markdown("""
    <div class="placeholder-card">
        <h3>🚧 개발 예정</h3>
        <p style="color: #78716c; font-size: 1.1rem;">
            Tabular 데이터 기반 MLP 모델이 아직 학습되지 않았습니다.
        </p>
        <hr style="border-color: rgba(217, 119, 6, 0.3); margin: 1.5rem 0;">
        <h4 style="color: #1e293b;">📋 계획된 내용</h4>
        <ul style="text-align: left; color: #334155;">
            <li>Tabular 데이터 기반 MLP 모델 설계 및 학습</li>
            <li>정규화, 드롭아웃, 조기 종료 적용</li>
            <li>ML 모델과 동일한 지표 기준 성능 비교</li>
        </ul>
        <h4 style="color: #1e293b; margin-top: 1.5rem;">📁 예상 Deliverable</h4>
        <p style="color: #78716c;">
            <code>/docs/02_training_report/02_dl_training_results.md</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 예상 구조 미리보기
    st.markdown("### 📐 예상 MLP 모델 구조 (참고용)")
    
    st.code("""
# MLP Model Architecture (예시)
class ChurnMLP(nn.Module):
    def __init__(self, input_dim, hidden_dims=[256, 128, 64]):
        super().__init__()
        
        layers = []
        prev_dim = input_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)
    """, language="python")


def show_model_comparison():
    """모델 비교 페이지"""
    import pandas as pd
    import json
    import plotly.graph_objects as go
    
    st.markdown("## ⚖️ 모델 비교")
    
    # 결과 로드
    try:
        with open("models/training_results.json", "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        st.error("학습 결과 파일을 찾을 수 없습니다.")
        return
    
    # CatBoost (Recall 최적화) 결과 로드 (있으면 비교에 포함)
    cb = None
    try:
        with open("models/recall_selected_results.json", "r") as f:
            cb = json.load(f)
    except FileNotFoundError:
        cb = None
    
    st.markdown("### 📊 전체 모델 성능 비교 (Test Set)")
    
    # 비교 테이블
    model_names = ["Logistic Regression", "LightGBM"]
    roc_list = [
        f"{results['Logistic Regression']['test_metrics']['roc_auc']:.4f}",
        f"{results['LightGBM']['test_metrics']['roc_auc']:.4f}",
    ]
    pr_list = [
        f"{results['Logistic Regression']['test_metrics']['pr_auc']:.4f}",
        f"{results['LightGBM']['test_metrics']['pr_auc']:.4f}",
    ]
    recall_list = [
        f"{results['Logistic Regression']['test_metrics']['recall']:.4f}",
        f"{results['LightGBM']['test_metrics']['recall']:.4f}",
    ]
    prec_list = [
        f"{results['Logistic Regression']['test_metrics']['precision']:.4f}",
        f"{results['LightGBM']['test_metrics']['precision']:.4f}",
    ]
    f1_list = [
        f"{results['Logistic Regression']['test_metrics']['f1']:.4f}",
        f"{results['LightGBM']['test_metrics']['f1']:.4f}",
    ]
    status_list = ["✅ 완료", "✅ 완료"]
    
    if cb is not None:
        cb_test = cb["test_metrics_optimal"]
        model_names.append("CatBoost (Recall Optimized)")
        roc_list.append(f"{cb_test['roc_auc']:.4f}")
        pr_list.append(f"{cb_test['pr_auc']:.4f}")
        recall_list.append(f"{cb_test['recall']:.4f}")
        prec_list.append(f"{cb_test['precision']:.4f}")
        f1_list.append(f"{cb_test['f1']:.4f}")
        status_list.append("✅ 완료")
    
    comparison_data = {
        "모델": model_names,
        "ROC-AUC": roc_list,
        "PR-AUC": pr_list,
        "Recall": recall_list,
        "Precision": prec_list,
        "F1-Score": f1_list,
        "상태": status_list,
    }
    
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 레이더 차트
    st.markdown("### 🎯 성능 레이더 차트")
    
    categories = ['ROC-AUC', 'PR-AUC', 'Recall', 'Precision', 'F1-Score']
    
    lr_test = results["Logistic Regression"]["test_metrics"]
    lgb_test = results["LightGBM"]["test_metrics"]
    cb_test = cb["test_metrics_optimal"] if cb is not None else None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[lr_test['roc_auc'], lr_test['pr_auc'], lr_test['recall'], lr_test['precision'], lr_test['f1']],
        theta=categories,
        fill='toself',
        name='Logistic Regression',
        line_color='#3b82f6'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[lgb_test['roc_auc'], lgb_test['pr_auc'], lgb_test['recall'], lgb_test['precision'], lgb_test['f1']],
        theta=categories,
        fill='toself',
        name='LightGBM',
        line_color='#8b5cf6'
    ))
    
    if cb_test is not None:
        fig.add_trace(go.Scatterpolar(
            r=[cb_test['roc_auc'], cb_test['pr_auc'], cb_test['recall'], cb_test['precision'], cb_test['f1']],
            theta=categories,
            fill='toself',
            name='CatBoost (Recall Optimized)',
            line_color='#a855f7'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0.4, 1],
                gridcolor='rgba(100, 116, 139, 0.3)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#1e293b'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 최적 모델 선정
    st.markdown("### 🏆 최적 모델 선정")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card" style="border-color: #86efac; background: #f0fdf4;">
            <h3 style="color: #166534;">🥇 추천 모델 (Baseline): LightGBM</h3>
            <h4 style="color: #1e293b;">선정 사유</h4>
            <ul style="color: #334155;">
                <li><strong>ROC-AUC 0.9887</strong>: Logistic Regression 대비 우수한 분류 성능</li>
                <li><strong>PR-AUC 0.9277</strong>: 불균형 데이터에서도 높은 정밀도-재현율 균형</li>
                <li><strong>Recall 0.9413</strong>: 이탈자의 94% 탐지</li>
            </ul>
            <h4 style="color: #1e293b;">주요 이탈 예측 피처</h4>
            <ol style="color: #334155;">
                <li><code>days_to_expire</code> - 만료일까지 남은 일수</li>
                <li><code>auto_renew_rate</code> - 자동 갱신 비율</li>
                <li><code>total_payment</code> - 총 결제액</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        if cb is not None:
            st.markdown("""
            <div class="info-card" style="border-color: #c4b5fd; background: #f5f3ff; margin-top: 1rem;">
                <h3 style="color: #4c1d95;">⭐ Recall 최적화 관점: CatBoost</h3>
                <p style="color: #4b5563;">
                    <strong>CatBoost (Recall Optimized)</strong>는 threshold를 조정하여<br/>
                    이탈 고객 Recall을 더욱 높인 모델입니다 (약 95% 수준).
                </p>
            </div>
            """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("#### LightGBM 성능 요약")
        st.metric("ROC-AUC", "0.9887", "Best")
        st.metric("PR-AUC", "0.9277", "Best")
        st.metric("Recall", "0.9413", "High")


def show_bm_strategy():
    """BM 전략 및 세그먼트 정의 페이지"""
    st.markdown("## 📌 BM 전략 / 세그먼트")
    
    st.markdown("""
    ### 1. 비즈니스 목표 (BM Goal)
    - **BM-1**: 다음 달 이탈 가능성이 높은 고객을 사전에 식별하여 **Retention 캠페인** 수행
    - **BM-2**: **LTV(총 결제액)가 높은 고객** 중 이탈 위험이 큰 그룹을 우선 타겟팅
    - **BM-3**: 자동갱신 해제 / 취소 이력이 있는 고객을 **집중 모니터링**하여 즉각 대응
    """)
    
    st.markdown("---")
    st.markdown("### 2. 핵심 지표 / Feature (LightGBM 기준 Top Features)")
    
    st.markdown("""
    - `days_to_expire` : 만료까지 남은 일수 (만료 임박 고객 = 높은 이탈 위험)
    - `auto_renew_rate` : 자동 갱신 비율 (OFF/낮음 = 높은 이탈 위험)
    - `total_payment` : 총 결제액 (높을수록 High Value 고객)
    - `cancel_count` : 취소 횟수 (불만/이탈 시도 신호)
    - `transaction_count`, `avg_discount_rate` 등 결제 행동 피처
    """)
    
    st.markdown("---")
    st.markdown("### 3. 세그먼트 정의 (Segments)")
    
    st.markdown("""
    **S1. High Value & High Risk (우선 타겟)**
    - 조건 예시:
      - 예측 이탈 확률 (Risk Score) ≥ 0.7
      - `total_payment` 상위 30%
    - 액션:
      - 고가 플랜 재구독 할인, 장기 구독 프로모션, VIP 전용 혜택 제안
    
    **S2. Auto-renew OFF & High/Medium Risk**
    - 조건 예시:
      - 자동 갱신 비율 `auto_renew_rate` 낮음 또는 최근 거래 `is_auto_renew_last = 0`
      - Risk Score ≥ 0.5
    - 액션:
      - 만료 전 리마인드, 자동 갱신 재설정 유도, 간편 결제/묶음 플랜 제안
    
    **S3. Usage 감소형 (Usage Drop형 위험 고객)**
    - 조건 예시:
      - 최근 7일 사용량이 30일 대비 감소: `secs_trend_w7_w30 < 0`, `days_trend_w7_w30 < 0`
      - 스킵율 증가: `skip_trend_w7_w30 > 0`
    - 액션:
      - 취향 기반 플레이리스트 추천, 신규 콘텐츠/테마 제안, 온보딩/리마인드 푸시
    """)
    
    st.markdown("---")
    st.markdown("### 4. 액션 매핑 요약")
    
    st.markdown("""
    | 세그먼트 | BM 관점 설명 | 권장 액션 |
    |---------|-------------|-----------|
    | S1 High Value & High Risk | 매출 기여도 높고, 이탈 시 손실이 큰 고객 | LTV 기반 VIP 케어, 고가/장기 플랜 인센티브 |
    | S2 Auto-renew OFF & Risk | 구독 의지가 약해졌거나 해제한 고객 | 만료 알림, 재구독/자동갱신 유도 캠페인 |
    | S3 Usage 감소형 | 최근 이용량이 줄어든 고객 | 콘텐츠 큐레이션, 취향 재탐색, 리텐션용 푸시/메일 |
    """)
    
    st.info(
        "실제 추론 페이지(🎯 추론 탭)에서는 입력된 Feature를 바탕으로 "
        "위 BM 세그먼트와 위험등급에 따라 간단한 추천 액션을 함께 제공합니다."
    )


def show_inference():
    """BM 규칙 기반 이탈 위험 추론 페이지"""
    import pandas as pd
    import numpy as np
    
    st.markdown("## 🎯 추론 (Inference)")
    
    st.markdown("""
    ### 🔍 BM 관점 이탈 위험 평가
    아래 주요 Feature 입력값을 기반으로, **BM 규칙 기반 Risk Score**를 계산하고
    위험 등급 및 추천 액션을 제안합니다.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📥 사용자 정보 입력 (요약 Feature)")
        
        days_to_expire = st.slider("만료까지 남은 일수 (days_to_expire)", 0, 365, 30)
        auto_renew_rate = st.slider("자동 갱신 비율 (auto_renew_rate)", 0.0, 1.0, 0.8)
        total_payment = st.number_input("총 결제액 (total_payment)", min_value=0, value=1500)
        cancel_count = st.number_input("취소 횟수 (cancel_count)", min_value=0, value=0)
        
        predict_btn = st.button("🔮 이탈 위험 예측", use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 이탈 위험 평가 결과")
        
        if predict_btn:
            # BM 규칙 기반 Risk Score 계산
            risk_score = min(
                1.0,
                max(
                    0.0,
                    0.3 * (1 - days_to_expire / 365)
                    + 0.3 * (1 - auto_renew_rate)
                    + 0.2 * (cancel_count / 5)
                    + 0.2 * (1 - min(total_payment, 5000) / 5000),
                ),
            )
            
            # 위험 등급 매핑
            if risk_score < 0.3:
                risk_level = "저위험"
                risk_color = "#22c55e"
                risk_emoji = "🟢"
            elif risk_score < 0.6:
                risk_level = "중위험"
                risk_color = "#fbbf24"
                risk_emoji = "🟡"
            else:
                risk_level = "고위험"
                risk_color = "#ef4444"
                risk_emoji = "🔴"
            
            st.markdown(
                f"""
            <div class="info-card" style="text-align: center; border-color: {risk_color};">
                <h2 style="font-size: 3rem; margin: 0;">{risk_emoji}</h2>
                <h3 style="color: {risk_color}; margin: 0.5rem 0;">{risk_level}</h3>
                <p style="font-size: 2rem; font-weight: bold; color: {risk_color};">
                    {risk_score:.1%}
                </p>
                <p style="color: #64748b; font-size: 0.9rem;">
                    BM 기반 이탈 위험 점수 (규칙 기반)
                </p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            
            # 세그먼트 및 추천 액션 결정
            segments = []
            actions = []
            
            # S1: High Value & High Risk
            if risk_score >= 0.7 and total_payment >= 1500:
                segments.append("S1 High Value & High Risk")
                actions.append(
                    "- LTV가 높은 고위험 고객입니다. VIP 전용 혜택, 장기 구독 할인, 재구독 인센티브 제공을 고려하세요."
                )
            
            # S2: Auto-renew OFF & Risk
            if risk_score >= 0.5 and auto_renew_rate <= 0.5:
                segments.append("S2 Auto-renew OFF & Risk")
                actions.append(
                    "- 자동 갱신 비율이 낮은 위험 고객입니다. 만료 전 리마인드 및 자동 갱신 재설정 유도 캠페인이 필요합니다."
                )
            
            # S3: Usage Drop형은 여기서는 측정 불가이므로 설명만 추가
            if not segments:
                segments.append("General Risk")
                actions.append(
                    "- 핵심 위험 신호는 있으나 특정 BM 세그먼트에 속하지 않습니다. "
                    "최근 사용량/스킵 패턴을 추가로 확인하여 Usage 감소형 여부를 판단하는 것이 좋습니다."
                )
            
            st.markdown("#### 📌 BM 세그먼트 판정")
            st.markdown(
                "<br>".join(f"- **{seg}**" for seg in segments),
                unsafe_allow_html=True,
            )
            
            st.markdown("#### 💡 추천 액션 (BM 관점)")
            for act in actions:
                st.markdown(act)
        else:
            st.markdown("""
            <div class="info-card" style="text-align: center;">
                <p style="color: #475569; font-size: 1.2rem;">
                    👈 사용자 정보를 입력하고<br/>예측 버튼을 클릭하세요
                </p>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

