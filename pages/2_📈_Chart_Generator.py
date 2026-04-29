"""
📈 Chart Generator — Create interactive charts with Plotly.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_custom_css, section_header, info_box
from utils.data_handler import (
    get_data, is_data_loaded, store_data, load_sample_data,
    get_numeric_columns, get_categorical_columns,
)

st.set_page_config(page_title="Chart Generator | Toolkit", page_icon="📈", layout="wide")
inject_custom_css()

section_header("📈 Chart Generator", "Build stunning interactive visualizations from your data")

# ── Check Data ──
if not is_data_loaded():
    info_box("No data loaded. Go to CSV Viewer to upload or load sample data.", "warning")
    if st.button("🧪 Load Sample Dataset"):
        store_data(load_sample_data())
        st.rerun()
    st.stop()

df = get_data()

# ── Dark Plotly Template ──
DARK_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(10,14,26,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        title=dict(font=dict(size=18, color="#e2e8f0")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.08)"),
        colorway=["#00D4FF", "#7B2FBE", "#FF0080", "#00E396", "#FFB020",
                   "#775DD0", "#FF4560", "#26a69a", "#FEB019", "#546E7A"],
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
)

CHART_TYPES = [
    "Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart",
    "Histogram", "Box Plot", "Violin Plot", "Area Chart", "Heatmap",
]

# ── Sidebar Config ──
with st.sidebar:
    st.markdown("### 🎨 Chart Settings")
    chart_type = st.selectbox("Chart Type", CHART_TYPES)
    st.markdown("---")

numeric_cols = get_numeric_columns(df)
cat_cols = get_categorical_columns(df)
all_cols = df.columns.tolist()

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ── Chart Configuration ──
config_col, chart_col = st.columns([1, 2.5])

with config_col:
    st.markdown("#### ⚙️ Configuration")

    if chart_type == "Heatmap":
        hm_cols = st.multiselect("Select numeric columns", numeric_cols, default=numeric_cols[:5])
        chart_title = st.text_input("Chart Title", f"Correlation Heatmap")
        color_scale = st.selectbox("Color Scale", ["Viridis", "Plasma", "Inferno", "Magma", "Cividis", "RdBu_r"])
    elif chart_type == "Pie Chart":
        values_col = st.selectbox("Values (numeric)", numeric_cols)
        names_col = st.selectbox("Labels", all_cols)
        chart_title = st.text_input("Chart Title", f"{values_col} by {names_col}")
        hole_size = st.slider("Donut hole", 0.0, 0.8, 0.4)
    elif chart_type == "Histogram":
        hist_col = st.selectbox("Column", numeric_cols)
        bins = st.slider("Number of bins", 5, 100, 30)
        chart_title = st.text_input("Chart Title", f"Distribution of {hist_col}")
        color_by = st.selectbox("Color by (optional)", ["None"] + cat_cols)
    elif chart_type in ("Box Plot", "Violin Plot"):
        y_col = st.selectbox("Y axis (numeric)", numeric_cols)
        x_col = st.selectbox("X axis (category)", ["None"] + cat_cols)
        chart_title = st.text_input("Chart Title", f"{chart_type}: {y_col}")
        color_by = st.selectbox("Color by", ["None"] + cat_cols)
    else:
        x_col = st.selectbox("X axis", all_cols)
        y_col = st.selectbox("Y axis", numeric_cols)
        chart_title = st.text_input("Chart Title", f"{y_col} vs {x_col}")
        color_by = st.selectbox("Color by (optional)", ["None"] + cat_cols)
        if chart_type == "Scatter Plot":
            size_by = st.selectbox("Size by (optional)", ["None"] + numeric_cols)

    opacity = st.slider("Opacity", 0.1, 1.0, 0.85)
    show_legend = st.checkbox("Show Legend", value=True)
    chart_height = st.slider("Chart Height", 300, 800, 500)

# ── Build Chart ──
with chart_col:
    st.markdown(f"#### 📊 {chart_type}")

    try:
        fig = None
        color_arg = color_by if color_by != "None" else None

        if chart_type == "Bar Chart":
            fig = px.bar(df, x=x_col, y=y_col, color=color_arg, title=chart_title,
                         opacity=opacity, barmode="group")
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x_col, y=y_col, color=color_arg, title=chart_title)
        elif chart_type == "Scatter Plot":
            size_arg = size_by if size_by != "None" else None
            fig = px.scatter(df, x=x_col, y=y_col, color=color_arg, size=size_arg,
                             title=chart_title, opacity=opacity)
        elif chart_type == "Pie Chart":
            fig = px.pie(df, values=values_col, names=names_col, title=chart_title, hole=hole_size)
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=hist_col, nbins=bins, color=color_arg if color_by != "None" else None,
                               title=chart_title, opacity=opacity)
        elif chart_type == "Box Plot":
            x_arg = x_col if x_col != "None" else None
            fig = px.box(df, x=x_arg, y=y_col, color=color_arg if color_by != "None" else None,
                         title=chart_title)
        elif chart_type == "Violin Plot":
            x_arg = x_col if x_col != "None" else None
            fig = px.violin(df, x=x_arg, y=y_col, color=color_arg if color_by != "None" else None,
                            title=chart_title, box=True)
        elif chart_type == "Area Chart":
            fig = px.area(df, x=x_col, y=y_col, color=color_arg, title=chart_title,
                          line_shape="spline")
        elif chart_type == "Heatmap":
            if len(hm_cols) >= 2:
                corr = df[hm_cols].corr()
                fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=color_scale,
                                title=chart_title, aspect="auto")
            else:
                st.warning("Select at least 2 numeric columns for the heatmap.")

        if fig is not None:
            fig.update_layout(
                template=DARK_TEMPLATE,
                height=chart_height,
                showlegend=show_legend,
                margin=dict(l=40, r=40, t=60, b=40),
            )
            st.plotly_chart(fig, use_container_width=True, key="main_chart")

            # Export buttons
            e1, e2 = st.columns(2)
            with e1:
                html_bytes = fig.to_html(include_plotlyjs="cdn").encode("utf-8")
                st.download_button("⬇️ Download as HTML", html_bytes, "chart.html", "text/html")
            with e2:
                img_bytes = fig.to_image(format="png", scale=2)
                st.download_button("🖼️ Download as PNG", img_bytes, "chart.png", "image/png")

    except Exception as e:
        st.error(f"Error generating chart: {e}")

# ── Side-by-Side Comparison ──
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

with st.expander("📊 Side-by-Side Chart Comparison"):
    st.markdown("Create two charts side by side for comparison.")
    comp1, comp2 = st.columns(2)

    with comp1:
        st.markdown("**Chart A**")
        ct_a = st.selectbox("Type", ["Histogram", "Box Plot", "Scatter Plot"], key="cta")
        col_a = st.selectbox("Column", numeric_cols, key="cola")
        if ct_a == "Histogram":
            fa = px.histogram(df, x=col_a, nbins=25, title=f"Histogram: {col_a}", opacity=0.8)
        elif ct_a == "Box Plot":
            fa = px.box(df, y=col_a, title=f"Box Plot: {col_a}")
        else:
            col_a2 = st.selectbox("Y axis", numeric_cols, key="cola2", index=min(1, len(numeric_cols)-1))
            fa = px.scatter(df, x=col_a, y=col_a2, title=f"{col_a2} vs {col_a}", opacity=0.7)
        fa.update_layout(template=DARK_TEMPLATE, height=350)
        st.plotly_chart(fa, use_container_width=True, key="comp_a")

    with comp2:
        st.markdown("**Chart B**")
        ct_b = st.selectbox("Type", ["Histogram", "Box Plot", "Scatter Plot"], key="ctb")
        col_b = st.selectbox("Column", numeric_cols, key="colb", index=min(1, len(numeric_cols)-1))
        if ct_b == "Histogram":
            fb = px.histogram(df, x=col_b, nbins=25, title=f"Histogram: {col_b}", opacity=0.8)
        elif ct_b == "Box Plot":
            fb = px.box(df, y=col_b, title=f"Box Plot: {col_b}")
        else:
            col_b2 = st.selectbox("Y axis", numeric_cols, key="colb2", index=min(2, len(numeric_cols)-1))
            fb = px.scatter(df, x=col_b, y=col_b2, title=f"{col_b2} vs {col_b}", opacity=0.7)
        fb.update_layout(template=DARK_TEMPLATE, height=350)
        st.plotly_chart(fb, use_container_width=True, key="comp_b")
