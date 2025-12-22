import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Setup Paths & Imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
model_dir = project_root / "03_trained_model"

sys.path.append(str(project_root / "src"))
sys.path.append(str(model_dir))

from ui_components import header, subheader, section_header, card, apply_global_styles

try:
    from model_inference import ModelInference
except ImportError:
    st.error("ModelInference module not found.")
    st.stop()

# Config
st.set_page_config(page_title="🎮 Marketing Simulator (타겟팅 및 시뮬레이션)", page_icon="🎮", layout="wide")

# --- Shared Logic ---
@st.cache_data
def load_and_score():
    try:
        data_path = project_root / "data/processed/kkbox_train_feature_v4.parquet"
        if not data_path.exists(): return None
        df = pd.read_parquet(data_path).sample(n=3000, random_state=42) # Sample for speed
        inf_v4 = ModelInference(model_dir=str(model_dir), model_version='v4')
        inf_v5 = ModelInference(model_dir=str(model_dir), model_version='v5.2')
        df['score_v4'] = inf_v4.predict(df)
        df['score_v5'] = inf_v5.predict(df)
        
        # Max Risk for Targeting (Primary Sort Key)
        df['max_risk'] = df[['score_v4', 'score_v5']].max(axis=1)
        
        # Mocking behavioral features if missing (for benchmarking demo)
        if 'listening_velocity' not in df.columns: df['listening_velocity'] = np.random.normal(0, 50, size=len(df))
        if 'secs_trend_w7_w30' not in df.columns: df['secs_trend_w7_w30'] = np.random.normal(-100, 100, size=len(df)) # Mock trend
        if 'active_decay_rate' not in df.columns: df['active_decay_rate'] = np.random.uniform(0.5, 1.5, size=len(df))
        
        return df
    except Exception as e:
        return None

def main():
    header("dashboard_customize", "마케팅 시뮬레이터 (Targeting Simulator)", "마케팅 범위 설정에 따른 실시간 위험 요인 및 전략 분석")
    apply_global_styles()
    
    df = load_and_score()
    if df is None: st.stop()
    df = df.copy() # Explicit copy to prevent cache mutation issues
    
    st.divider()
    
    # 3.1 Targeting Control
    subheader("tune", "3.1 타겟 범위 설정 (Real-time Simulation)")
    
    col_ctrl, col_matrix = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown('<div style="display: flex; align-items: center; margin-bottom:10px; color:#1976D2;"><span class="material-icons" style="margin-right:5px;">touch_app</span> <strong>슬라이더를 조절해 보세요</strong></div>', unsafe_allow_html=True)
        
        # 1. Targeting Scope
        top_n = st.slider("1. 이탈 위험 상위 N% 타겟팅 (Scope)", 1, 100, 20)
        
        # 2. Sensitivity Threshold
        sensitivity = st.slider("2. 위험 민감도 (Sensitivity)", 0.1, 0.9, 0.5, 0.05, 
                              help="낮출수록 더 많은 유저를 '위험'으로 간주합니다. (0.3 = 민감/공격적 방어, 0.7 = 둔감/보수적)")
        
        # Logic Application
        threshold_val = np.percentile(df['max_risk'], 100 - top_n)
        df['is_target'] = df['max_risk'] >= threshold_val
        
        # Dynamic Segment Assignment based on Sensitivity
        def assign_segment(row):
            v4, v5 = row['score_v4'], row['score_v5']
            # Use sensitivity slider as the threshold
            th = sensitivity 
            if v4 < th and v5 < th: return 'Safety'
            elif v4 < th and v5 >= th: return 'Watch-out'
            elif v4 >= th and v5 < th: return 'Warning'
            else: return 'Danger'
            
        df['segment'] = df.apply(assign_segment, axis=1)
        
        target_df = df[df['is_target']]
        normal_df = df[~df['is_target']]
        
        # KPI Cards
        section_header("insights", "Simulation KPIs")
        c1, c2 = st.columns(2)
        c1.metric("타겟 유저", f"{len(target_df):,}명", f"{top_n}%")
        
        risk_diff = 0
        if not normal_df.empty and not target_df.empty:
             risk_diff = target_df['max_risk'].mean() - normal_df['max_risk'].mean()
        
        target_risk_mean = target_df['max_risk'].mean() if not target_df.empty else 0
        c2.metric("평균 Risk", f"{target_risk_mean:.2f}", f"+{risk_diff:.2f}")
                  
    with col_matrix:
        section_header("search", "실시간 4분면 하이라이트")
        
        # Prepare Plot Data
        plot_df = df.copy()
        plot_df['status'] = plot_df['is_target'].apply(lambda x: 'Attributes: Selected Target' if x else 'Attributes: Normal User')
        
        fig = px.scatter(
            plot_df, x='score_v5', y='score_v4',
            color='status',
            color_discrete_map={
                'Attributes: Selected Target': '#FF4B4B', # Red
                'Attributes: Normal User': '#E0E0E0'      # Gray
            },
            opacity=0.6,
            labels={'score_v5': '행동 위험도 (V5.2)', 'score_v4': '이력 위험도 (V4)'},
            hover_data=['score_v4', 'score_v5']
        )
        
        # Add Dynamic Quadrant Lines defined by Sensitivity
        fig.add_vline(x=sensitivity, line_dash="dash", line_color="black", annotation_text=f"Threshold {sensitivity}")
        fig.add_hline(y=sensitivity, line_dash="dash", line_color="black")
        
        # Annotations for Quadrants
        fig.add_annotation(x=sensitivity/2, y=sensitivity/2, text="Safe", showarrow=False, font=dict(color="green", size=24, family="Arial Black"))
        fig.add_annotation(x=(1+sensitivity)/2, y=(1+sensitivity)/2, text="Danger", showarrow=False, font=dict(color="red", size=24, family="Arial Black"))
        
        fig.update_layout(height=500, margin=dict(t=20, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 3.2 Benchmarking (Lift Analysis)
    subheader("compare_arrows", "5.2 타겟 위험 요인 벤치마킹 (Benchmarking)")
    
    # Explanation
    st.markdown("""
    <div style="background-color: #F5F5F5; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 0.9rem;">
        <strong style="color: #333;">그룹 정의 (Group Definitions):</strong>
        <ul style="margin: 5px 0 0 20px; color: #555;">
            <li><strong>Target (타겟 그룹)</strong>: 위에서 설정한 타겟팅 조건(상위 N%)에 해당하는 고위험 유저군입니다.</li>
            <li><strong>Normal (일반 그룹)</strong>: 타겟팅 되지 않은 나머지 일반 유저군입니다.</li>
            <li><strong>Global (전체 평균)</strong>: 전체 유저의 평균값입니다.</li>
        </ul>
        <p style="margin: 8px 0 0 0; color: #666;">※ 아래 차트는 <strong>Target vs Normal</strong> 간의 핵심 지표 차이를 보여줍니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if target_df.empty or normal_df.empty:
        st.warning("비교할 타겟 또는 일반 그룹 데이터가 부족합니다.")
    else:
        # Prepare Data for Chart
        metrics = [
            {"label": "활동 감소율 (Decay)", "col": "active_decay_rate", "desc": "낮을수록 활동 급감"},
            {"label": "청취 변화 (Trend)", "col": "secs_trend_w7_w30", "desc": "음수일수록 청취 시간 급감"},
            {"label": "위험 점수 (Risk)", "col": "max_risk", "desc": "최대 이탈 위험도"}
        ]
        
        bench_data = []
        for m in metrics:
            bench_data.append({"Metric": m['label'], "Group": "Target", "Value": target_df[m['col']].mean()})
            bench_data.append({"Metric": m['label'], "Group": "Normal", "Value": normal_df[m['col']].mean()})
            
        bench_df = pd.DataFrame(bench_data)
        
        # Grouped Bar Chart
        fig_bench = px.bar(bench_df, x="Metric", y="Value", color="Group", barmode="group",
                           title="Target vs Normal 핵심 지표 비교",
                           color_discrete_map={"Target": "#FF5252", "Normal": "#90CAF9"},
                           text_auto='.2f')
        
        fig_bench.update_layout(height=400, xaxis_title=None, yaxis_title="Average Value",
                                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        
        st.plotly_chart(fig_bench, use_container_width=True, key=f"bench_chart_{top_n}")
        
        # Text Insights
        c_i1, c_i2, c_i3 = st.columns(3)
        
        def show_insight_metric(col, label, key_col, inverse=False):
            t_val = target_df[key_col].mean()
            n_val = normal_df[key_col].mean()
            diff = t_val - n_val
            
            # Color logic
            is_bad = (diff > 0 and not inverse) or (diff < 0 and inverse)
            color = "#D32F2F" if is_bad else "#388E3C"
            arrow = "▲" if diff > 0 else "▼"
            
            col.metric(label, f"{t_val:.2f}", f"{arrow} {abs(diff):.2f} (vs Normal)", delta_color="inverse" if inverse else "normal")

        show_insight_metric(c_i1, "활동 감소율 (Decay)", "active_decay_rate", inverse=True)
        show_insight_metric(c_i2, "청취 변화 (Trend)", "secs_trend_w7_w30", inverse=True) # Negative trend is bad (Inverse)
        show_insight_metric(c_i3, "이탈 위험도 (Score)", "max_risk", inverse=False)
    
    st.divider()

    # 3.3 Target Composition & Action Plan
    col_comp, col_act = st.columns([2, 1])
    
    with col_comp:
        subheader("pie_chart", "타겟 구성비 (Composition)")
        
        # Calculate Segment Counts for Target DF using NEW sensitivity
        
        if not target_df.empty:
            fig_pie = px.pie(target_df, names='segment', title="선택된 그룹의 세그먼트 분포", 
                             color='segment',
                             color_discrete_map={'Safety': '#E8F5E9', 'Watch-out': '#FFFDE7', 'Warning': '#FFF3E0', 'Danger': '#FFEBEE'})
            
            fig_pie.update_traces(textposition='auto', textinfo='percent+label', textfont_size=20)
            fig_pie.update_layout(
                height=450, 
                margin=dict(t=40, b=10, l=10, r=10),
                legend=dict(font=dict(size=15)),
                title=dict(font=dict(size=20))
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("선택된 타겟 유저가 없습니다.")

    with col_act:
        subheader("medical_services", "맞춤형 자동 처방 (Auto-Prescription)")
        
        if target_df.empty:
            st.info("타겟 유저가 선택되지 않았습니다.")
        else:
            seg_counts = target_df['segment'].value_counts()
            
            # Show all segments that exist in the target (count > 0)
            if seg_counts.get('Danger', 0) > 0:
                card("dangerous", f"위험 지대 (Danger) ({seg_counts.get('Danger',0):,}명)", 
                     ["즉시 이탈 위험이 매우 높습니다.", "Action: 1개월 무료 쿠폰 즉시 발송."], 
                     "#FFEBEE", "#FF5252")
            
            if seg_counts.get('Warning', 0) > 0:
                card("warning", f"경보 지대 (Warning) ({seg_counts.get('Warning',0):,}명)",
                     ["이력은 불안하나 행동은 아직 유지 중입니다.", "Action: 결제 수단 업데이트 및 혜택 안내."],
                     "#FFF3E0", "#FF9800")
            
            if seg_counts.get('Watch-out', 0) > 0:
                card("visibility", f"주의 지대 (Watch-out) ({seg_counts.get('Watch-out',0):,}명)",
                     ["결제는 안정적이나 최근 활동이 급감했습니다.", "Action: 신규 콘텐츠 푸시 및 Engagement 유도."],
                     "#FFFDE7", "#FBC02D")
            
            if seg_counts.get('Safety', 0) > 0:
                card("verified", f"안전 지대 (Safe) ({seg_counts.get('Safety',0):,}명)",
                     ["이탈 위험이 매우 낮습니다.", "Action: 마케팅 제외 권장 (비용 절감)."],
                     "#E8F5E9", "#4CAF50")

    st.divider()
    csv = target_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("타겟 유저 리스트 다운로드 (CSV)", csv, "target_users.csv", "text/csv", use_container_width=True)

if __name__ == "__main__":
    main()
