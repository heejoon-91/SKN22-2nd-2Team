import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import textwrap
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
st.set_page_config(page_title="Risk Matrix Dashboard", page_icon="📈", layout="wide")

# --- Shared Logic ---
@st.cache_data
def load_and_score():
    """Load data and predict with both models to create the matrix"""
    try:
        data_path = project_root / "data/processed/kkbox_train_feature_v4.parquet"
        if not data_path.exists(): return None
        
        # Load sample
        df = pd.read_parquet(data_path).sample(n=2000, random_state=42)
        
        # Load models
        inf_v4 = ModelInference(model_dir=str(model_dir), model_version='v4')
        inf_v5 = ModelInference(model_dir=str(model_dir), model_version='v5.2')
        
        # Predict
        df['score_v4'] = inf_v4.predict(df)
        df['score_v5'] = inf_v5.predict(df)
        
        # Define Segments
        def assign_segment(row):
            v4, v5 = row['score_v4'], row['score_v5']
            if v4 < 0.5 and v5 < 0.5: return '1. 안전 지대 (Safe)'
            elif v4 < 0.5 and v5 >= 0.5: return '2. 주의 지대 (Watch-out)'
            elif v4 >= 0.5 and v5 < 0.5: return '3. 경보 지대 (Warning)'
            else: return '4. 위험 지대 (Danger)'
            
        df['segment'] = df.apply(assign_segment, axis=1)
        return df
    except Exception as e:
        st.error(f"Data scoring error: {e}")
        return None

def main():
    header("grid_view", "위험도 매트릭스 (Risk Matrix)", "행동(심리)과 이력(상태)의 결합을 통한 입체적 세그멘테이션")
    apply_global_styles()
    
    df = load_and_score()
    if df is None: st.stop()
    
    st.divider()
    
    # 2.1 4-Quadrant Analysis
    col_plot, col_info = st.columns([2, 1])
    
    with col_plot:
        subheader("scatter_plot", "2.1 4분면 매트릭스 (Action-Oriented)")
        
        fig = px.scatter(
            df, x='score_v5', y='score_v4',
            color='segment',
            color_discrete_map={
                '1. 안전 지대 (Safe)': '#4CAF50',   # Strong Green
                '2. 주의 지대 (Watch-out)': '#FFD600', # Yellow
                '3. 경보 지대 (Warning)': '#FF9800',   # Strong Orange
                '4. 위험 지대 (Danger)': '#FF5252'     # Strong Red
            },
            hover_data=['score_v4', 'score_v5'],
            labels={'score_v5': '행동 위험도 (V5.2: 마음)', 'score_v4': '이력 위험도 (V4: 상태)'},
            category_orders={'segment': ['1. 안전 지대 (Safe)', '2. 주의 지대 (Watch-out)', '3. 경보 지대 (Warning)', '4. 위험 지대 (Danger)']}
        )

        # Update traces for better visibility
        fig.update_traces(marker=dict(size=8, opacity=0.3))
        
        # Add Quadrant Lines
        fig.add_vline(x=0.5, line_dash="dash", line_color="#9E9E9E", opacity=0.8)
        fig.add_hline(y=0.5, line_dash="dash", line_color="#9E9E9E", opacity=0.8)
        
        # Add Labels to Quadrants (Larger and Bold, Color synced with Cards)
        # Safe: #4CAF50, Watch-out: #FBC02D, Warning: #FF9800, Danger: #FF5252
        fig.add_annotation(x=0.25, y=0.25, text="Safe", showarrow=False, font=dict(color="#4CAF50", size=24, family="Arial Black"))
        fig.add_annotation(x=0.75, y=0.25, text="Watch-out", showarrow=False, font=dict(color="#FBC02D", size=24, family="Arial Black"))
        fig.add_annotation(x=0.25, y=0.75, text="Warning", showarrow=False, font=dict(color="#FF9800", size=24, family="Arial Black"))
        fig.add_annotation(x=0.75, y=0.75, text="Danger", showarrow=False, font=dict(color="#FF5252", size=30, family="Arial Black"))
        
        fig.update_layout(height=600, showlegend=True, legend_title_text='고객 그룹', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        subheader("strategy", "2.2 전략적 그룹 정의")
        
        card("verified", "안전 지대 (Safe)", ["상태: 충성도 높음", "전략: Lock-in 전략 및 신규 기능 체험"], "#E8F5E9", "#4CAF50")
        card("visibility", "주의 지대 (Watch-out)", ["상태: 결제 유지 중이나 활동 급감", "전략: Engagement 푸시 (콘텐츠 기반)"], "#FFFDE7", "#FBC02D")
        card("warning", "경보 지대 (Warning)", ["상태: 활동은 있으나 결제 이력 불안", "전략: 결제 수단 업데이트 혜택"], "#FFF3E0", "#FF9800")
        card("dangerous", "위험 지대 (Danger)", ["상태: 활동 전무, 해지 징후 뚜렷", "전략: Win-back 프로모션 (쿠폰)"], "#FFEBEE", "#FF5252")

        st.divider()
        section_header("lightbulb", "인사이트")
        counts = df['segment'].value_counts()
        total = len(df)
        danger_ratio = counts.get('4. 위험 지대 (Danger)', 0)/total*100
        st.write(f"- 전체 대상: {total:,}명")
        st.metric("위험 지대 (Danger) 비중", f"{danger_ratio:.1f}%", f"{int(total * danger_ratio / 100):,}명")

if __name__ == "__main__":
    main()
