"""
📊 CSV Viewer — Upload, preview, filter, search, and export data.
"""

import streamlit as st
import pandas as pd
from utils.theme import inject_custom_css, section_header, metric_card, info_box
from utils.data_handler import (
    load_file, store_data, get_data, is_data_loaded,
    get_numeric_columns, get_categorical_columns,
    get_memory_usage, get_missing_percentage, load_sample_data,
)

st.set_page_config(page_title="CSV Viewer | Toolkit", page_icon="📊", layout="wide")
inject_custom_css()

section_header("📊 CSV Viewer", "Upload, explore, filter, and export your data")

# ── Upload Section ──
uploaded_file = st.file_uploader(
    "Drop your file here",
    type=["csv", "xlsx", "xls", "tsv"],
    help="Supported formats: CSV, Excel (xlsx/xls), TSV",
)

if uploaded_file is not None:
    try:
        df = load_file(uploaded_file)
        store_data(df)
        st.toast(f"✅ Loaded {uploaded_file.name}", icon="📂")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# Load sample if nothing loaded
if not is_data_loaded():
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    info_box("No data loaded yet. Upload a file above or load the sample dataset.", "info")
    if st.button("🧪 Load Sample Dataset"):
        df = load_sample_data()
        store_data(df)
        st.rerun()
    st.stop()

df = get_data()

# ── Quick Stats Bar ──
st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    metric_card("Rows", f"{df.shape[0]:,}", "📋")
with m2:
    metric_card("Columns", f"{df.shape[1]}", "📐")
with m3:
    metric_card("Numeric", f"{len(get_numeric_columns(df))}", "🔢")
with m4:
    metric_card("Memory", get_memory_usage(df), "💾")
with m5:
    metric_card("Missing %", f"{get_missing_percentage(df)}%", "⚠️")

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ── Tabs ──
tab_preview, tab_filter, tab_inspect = st.tabs(["🔍 Data Preview", "🎯 Filter & Search", "🧬 Column Inspector"])

# ── Tab 1: Data Preview ──
with tab_preview:
    st.markdown("##### Full Dataset")
    st.dataframe(df, use_container_width=True, height=450)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Full CSV", csv_data, "data_export.csv", "text/csv")

# ── Tab 2: Filter & Search ──
with tab_filter:
    st.markdown("##### Apply Filters")
    filtered_df = df.copy()

    # Text search
    search = st.text_input("🔎 Search across all columns", placeholder="Type to search...")
    if search:
        mask = filtered_df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False))
        filtered_df = filtered_df[mask.any(axis=1)]

    # Column filters
    filter_cols = st.multiselect("Select columns to filter", df.columns.tolist())

    for col in filter_cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            min_v, max_v = float(df[col].min()), float(df[col].max())
            selected = st.slider(f"Range: {col}", min_v, max_v, (min_v, max_v), key=f"slider_{col}")
            filtered_df = filtered_df[(filtered_df[col] >= selected[0]) & (filtered_df[col] <= selected[1])]
        else:
            options = df[col].dropna().unique().tolist()
            selected = st.multiselect(f"Values: {col}", options, default=options, key=f"multi_{col}")
            filtered_df = filtered_df[filtered_df[col].isin(selected)]

    # Sorting
    sort_col = st.selectbox("Sort by column", ["(none)"] + df.columns.tolist())
    if sort_col != "(none)":
        sort_order = st.radio("Order", ["Ascending", "Descending"], horizontal=True)
        filtered_df = filtered_df.sort_values(sort_col, ascending=(sort_order == "Ascending"))

    # Show results
    st.markdown(f"**Showing {len(filtered_df):,} of {len(df):,} rows**")
    st.dataframe(filtered_df, use_container_width=True, height=400)

    csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Filtered CSV", csv_filtered, "filtered_export.csv", "text/csv")

# ── Tab 3: Column Inspector ──
with tab_inspect:
    st.markdown("##### Column Details")

    col_info = []
    for col in df.columns:
        col_info.append({
            "Column": col,
            "Type": str(df[col].dtype),
            "Non-Null": int(df[col].notna().sum()),
            "Null": int(df[col].isna().sum()),
            "Unique": int(df[col].nunique()),
            "Sample": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "—",
        })

    info_df = pd.DataFrame(col_info)
    st.dataframe(info_df, use_container_width=True, hide_index=True)

    # Detailed view per column
    selected_col = st.selectbox("Inspect column", df.columns.tolist())
    if selected_col:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Data Type:** `{df[selected_col].dtype}`")
            st.markdown(f"**Unique Values:** {df[selected_col].nunique()}")
            st.markdown(f"**Missing:** {df[selected_col].isna().sum()} ({df[selected_col].isna().mean()*100:.1f}%)")
        with c2:
            if pd.api.types.is_numeric_dtype(df[selected_col]):
                st.markdown(f"**Min:** {df[selected_col].min()}")
                st.markdown(f"**Max:** {df[selected_col].max()}")
                st.markdown(f"**Mean:** {df[selected_col].mean():.2f}")
            else:
                top_vals = df[selected_col].value_counts().head(5)
                st.markdown("**Top Values:**")
                for val, cnt in top_vals.items():
                    st.markdown(f"- `{val}`: {cnt}")
