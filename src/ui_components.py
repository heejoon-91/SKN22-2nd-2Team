import streamlit as st
import textwrap
from pathlib import Path

def apply_global_styles():
    """
    Applies global CSS from assets/style.css and loads Material Icons.
    """
    # Assuming assets is at the project root, and ui_components is in src/
    # Project Root = src/../
    project_root = Path(__file__).parent.parent
    css_path = project_root / "assets/style.css"
    
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

def header(icon, title, subtitle=None):
    """
    Renders a consistent Page Header with Material Icon.
    """
    st.markdown(f'<h1 style="display: flex; align-items: center;"><span class="material-icons" style="font-size: 2.5rem; margin-right: 15px;">{icon}</span> {title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"**{subtitle}**")

def subheader(icon, title):
    """
    Renders a consistent Subheader with Material Icon.
    """
    st.markdown(f'<h3 style="display: flex; align-items: center;"><span class="material-icons" style="margin-right: 10px;">{icon}</span> {title}</h3>', unsafe_allow_html=True)

def section_header(icon, title):
    """
    Renders a smaller section header (H4 style).
    """
    st.markdown(f'<h4 style="display: flex; align-items: center;"><span class="material-icons" style="margin-right: 8px;">{icon}</span> {title}</h4>', unsafe_allow_html=True)

import re

def card(icon, title, content_list, bg_color, border_color, text_color="#333333"):
    """
    Renders a styled card with an icon, title, and list of contents.
    Used for prescriptions, insights, etc.
    """
    def parse_markdown(text):
        # Replace **text** with <strong>text</strong>
        return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

    # content_list can be a list of strings (bullets) or a single string
    if isinstance(content_list, list):
        items_html = "".join([f"<li>{parse_markdown(item)}</li>" for item in content_list])
        content_html = f'<ul style="margin: 5px 0 0 20px; font-size: 0.95rem; color: {text_color};">{items_html}</ul>'
    else:
        content_html = f'<p style="font-size: 0.95rem; margin: 5px 0; color: {text_color};">{parse_markdown(content_list)}</p>'

    st.markdown(textwrap.dedent(f"""
    <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid {border_color};">
        <strong style="color: {border_color}; display: flex; align-items: center;">
            <span class="material-icons" style="margin-right: 8px;">{icon}</span> {title}
        </strong>
        {content_html}
    </div>
    """), unsafe_allow_html=True)

def metric_card(icon, label, value, description=None, color="#4a90e2", bg_color="#f8f9fa"):
    """
    Renders a metric card with an icon, label, and value.
    """
    desc_html = f'<p style="font-size: 0.8rem; color: #666; margin: 4px 0 0 0;">{description}</p>' if description else ""
    
    st.markdown(textwrap.dedent(f"""
    <div style="background-color: {bg_color}; padding: 16px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.08); box-shadow: 0 2px 4px rgba(0,0,0,0.03); margin-bottom: 20px;">
        <div style="display: flex; align-items: start; margin-bottom: 8px;">
            <div style="background-color: {color}20; padding: 8px; border-radius: 8px; color: {color}; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
                <span class="material-icons" style="font-size: 1.5rem;">{icon}</span>
            </div>
            <div>
                <p style="font-size: 0.85rem; font-weight: 600; color: #555; margin: 0;">{label}</p>
                <p style="font-size: 1.1rem; font-weight: 700; color: #333; margin: 4px 0 0 0;">{value}</p>
                {desc_html}
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)
