"""
Custom theme and styling utilities for the Data Analysis Toolkit.
Provides a premium dark theme with glassmorphism, gradient accents, and animations.
"""

import streamlit as st


def inject_custom_css():
    """Inject the full custom CSS theme into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def metric_card(label: str, value, icon: str = "📊", delta: str = None):
    """Render a glassmorphism-style metric card."""
    delta_html = ""
    if delta is not None:
        color = "#00E396" if not delta.startswith("-") else "#FF4560"
        delta_html = f'<div style="color:{color}; font-size:0.85rem; margin-top:4px;">{delta}</div>'

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    """Render a styled section header with optional subtitle."""
    sub_html = f'<p style="color: #8892b0; font-size: 1rem; margin-top: 4px;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="
            background: linear-gradient(135deg, #00D4FF, #7B2FBE, #FF0080);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0;
        ">{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def info_box(text: str, box_type: str = "info"):
    """Render a styled info/warning/success box."""
    colors = {
        "info": ("#00D4FF", "rgba(0, 212, 255, 0.08)", "ℹ️"),
        "success": ("#00E396", "rgba(0, 227, 150, 0.08)", "✅"),
        "warning": ("#FFB020", "rgba(255, 176, 32, 0.08)", "⚠️"),
        "error": ("#FF4560", "rgba(255, 69, 96, 0.08)", "❌"),
    }
    accent, bg, icon = colors.get(box_type, colors["info"])
    st.markdown(f"""
    <div style="
        background: {bg};
        border-left: 4px solid {accent};
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        color: #ccd6f6;
        font-size: 0.95rem;
    ">
        {icon} {text}
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────────────────────
# Full Custom CSS
# ────────────────────────────────────────────
CUSTOM_CSS = """
<style>
    /* ── Import Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0e1a;
        --bg-secondary: #111827;
        --bg-card: rgba(17, 24, 39, 0.7);
        --bg-card-hover: rgba(17, 24, 39, 0.9);
        --text-primary: #e2e8f0;
        --text-secondary: #8892b0;
        --accent-cyan: #00D4FF;
        --accent-purple: #7B2FBE;
        --accent-magenta: #FF0080;
        --accent-green: #00E396;
        --border-subtle: rgba(255, 255, 255, 0.06);
        --glow-cyan: 0 0 20px rgba(0, 212, 255, 0.15);
        --glow-purple: 0 0 20px rgba(123, 47, 190, 0.15);
    }

    /* ── Global Styles ── */
    .stApp {
        background: var(--bg-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1321 0%, #111827 100%) !important;
        border-right: 1px solid var(--border-subtle) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--text-primary) !important;
    }

    /* ── Headers ── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary) !important;
    }

    /* ── Animated Gradient Title ── */
    .gradient-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D4FF, #7B2FBE, #FF0080, #00D4FF);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 6s ease infinite;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.4rem 1.5rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple), var(--accent-magenta));
        border-radius: 16px 16px 0 0;
    }

    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 212, 255, 0.2);
        box-shadow: var(--glow-cyan);
    }

    .metric-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--text-primary);
    }

    /* ── Feature Cards ── */
    .feature-card {
        background: var(--bg-card);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-6px);
        box-shadow: var(--glow-purple);
        border-color: rgba(123, 47, 190, 0.3);
    }

    .feature-card h3 {
        font-size: 1.2rem;
        margin: 0.8rem 0 0.5rem 0;
        color: var(--text-primary) !important;
    }

    .feature-card p {
        color: var(--text-secondary);
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .feature-icon {
        font-size: 2.2rem;
        display: inline-block;
    }

    /* ── Dataframe Styling ── */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.6rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.02em;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.3) !important;
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00E396, #00B4D8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 227, 150, 0.3) !important;
    }

    /* ── Selectbox / Inputs ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* ── File Uploader ── */
    .stFileUploader > div {
        border: 2px dashed rgba(0, 212, 255, 0.3) !important;
        border-radius: 16px !important;
        background: rgba(0, 212, 255, 0.03) !important;
        transition: all 0.3s ease !important;
    }

    .stFileUploader > div:hover {
        border-color: rgba(0, 212, 255, 0.5) !important;
        background: rgba(0, 212, 255, 0.06) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-secondary) !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(123, 47, 190, 0.15)) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
        color: var(--text-primary) !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: var(--border-subtle) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(0, 212, 255, 0.2);
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 212, 255, 0.4);
    }

    /* ── Glow Divider ── */
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), var(--accent-magenta), transparent);
        border: none;
        margin: 2rem 0;
        border-radius: 2px;
    }

    /* ── Badge ── */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .badge-cyan {
        background: rgba(0, 212, 255, 0.12);
        color: var(--accent-cyan);
        border: 1px solid rgba(0, 212, 255, 0.25);
    }

    .badge-purple {
        background: rgba(123, 47, 190, 0.12);
        color: #a855f7;
        border: 1px solid rgba(123, 47, 190, 0.25);
    }

    .badge-magenta {
        background: rgba(255, 0, 128, 0.12);
        color: var(--accent-magenta);
        border: 1px solid rgba(255, 0, 128, 0.25);
    }
</style>
"""
