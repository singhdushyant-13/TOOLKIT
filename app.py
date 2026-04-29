"""
Data Analysis Toolkit — Main Entry Point
A premium Streamlit-based data analysis suite.
"""

import streamlit as st
from utils.theme import inject_custom_css
from utils.data_handler import load_sample_data, store_data

# ── Page Config ──
st.set_page_config(
    page_title="Data Analysis Toolkit",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Theme ──
inject_custom_css()

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 🔬 Data Toolkit")
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    **Navigation**
    
    Use the pages in the sidebar to:
    - 📊 **View & Filter** your data
    - 📈 **Generate Charts** interactively
    - 🔢 **Compute Statistics** & insights
    """)
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#8892b0; font-size:0.8rem;">Built with Streamlit + Plotly</p>',
        unsafe_allow_html=True,
    )

# ── Hero Section ──
st.markdown('<div class="gradient-title">Data Analysis Toolkit</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#8892b0; font-size:1.15rem; margin-top:0; margin-bottom:2rem;">'
    "Upload your dataset and explore it with powerful visualization, filtering, and statistical analysis tools."
    "</p>",
    unsafe_allow_html=True,
)

# ── Feature Cards ──
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>CSV Viewer</h3>
        <p>Upload CSV or Excel files, preview data in an interactive table, filter by columns, search rows, and export filtered results.</p>
        <span class="badge badge-cyan">EXPLORE</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <h3>Chart Generator</h3>
        <p>Create stunning interactive charts — line, bar, scatter, pie, histogram, box plot, heatmap, area, and violin plots.</p>
        <span class="badge badge-purple">VISUALIZE</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔢</div>
        <h3>Statistics Calculator</h3>
        <p>Compute descriptive statistics, correlation matrices, distribution analysis, hypothesis tests, and outlier detection.</p>
        <span class="badge badge-magenta">ANALYZE</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ── Quick Start ──
st.markdown("""
<h3 style="color:#e2e8f0;">⚡ Quick Start</h3>
""", unsafe_allow_html=True)

qcol1, qcol2 = st.columns([1, 1])

with qcol1:
    st.markdown("""
    <div style="
        background: rgba(17,24,39,0.7);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
    ">
        <h4 style="color:#00D4FF; margin-top:0;">📂 Upload Your Data</h4>
        <p style="color:#8892b0; font-size:0.95rem;">
            Go to the <strong>CSV Viewer</strong> page and upload a CSV or Excel file.
            Your data will be available across all pages.
        </p>
    </div>
    """, unsafe_allow_html=True)

with qcol2:
    st.markdown("""
    <div style="
        background: rgba(17,24,39,0.7);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
    ">
        <h4 style="color:#7B2FBE; margin-top:0;">🧪 Try Sample Data</h4>
        <p style="color:#8892b0; font-size:0.95rem;">
            No data? Click below to load a sample employee dataset
            and start exploring immediately.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
if st.button("🚀 Load Sample Dataset", use_container_width=False):
    df = load_sample_data()
    store_data(df)
    st.success(f"✅ Sample data loaded! {df.shape[0]} rows × {df.shape[1]} columns. Navigate to any page to explore.")
    st.dataframe(df.head(10), use_container_width=True)
