"""
🔢 Statistics — Descriptive stats, correlations, distributions, and outlier detection.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import inject_custom_css, section_header, metric_card, info_box
from utils.data_handler import (
    get_data, is_data_loaded, store_data, load_sample_data,
    get_numeric_columns, get_categorical_columns,
)

st.set_page_config(page_title="Statistics | Toolkit", page_icon="🔢", layout="wide")
inject_custom_css()

section_header("🔢 Statistics Calculator", "Deep statistical analysis of your data")

DARK_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(10,14,26,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        colorway=["#00D4FF", "#7B2FBE", "#FF0080", "#00E396", "#FFB020",
                   "#775DD0", "#FF4560", "#26a69a", "#FEB019", "#546E7A"],
    )
)

if not is_data_loaded():
    info_box("No data loaded. Go to CSV Viewer to upload or load sample data.", "warning")
    if st.button("🧪 Load Sample Dataset"):
        store_data(load_sample_data())
        st.rerun()
    st.stop()

df = get_data()
numeric_cols = get_numeric_columns(df)
cat_cols = get_categorical_columns(df)

# ── Tabs ──
tab_desc, tab_corr, tab_dist, tab_hypo, tab_missing, tab_outlier = st.tabs([
    "📋 Descriptive", "🔗 Correlation", "📊 Distribution",
    "🧪 Hypothesis Tests", "❓ Missing Data", "🎯 Outliers",
])

# ══════════════════════════════════════════
# Tab 1: Descriptive Statistics
# ══════════════════════════════════════════
with tab_desc:
    st.markdown("##### Descriptive Statistics — Numeric Columns")

    if numeric_cols:
        desc = df[numeric_cols].describe().T
        desc["skewness"] = df[numeric_cols].skew()
        desc["kurtosis"] = df[numeric_cols].kurtosis()
        desc = desc.round(3)
        st.dataframe(desc, use_container_width=True)

        # Individual column detail
        st.markdown("---")
        sel_col = st.selectbox("Detailed view for column:", numeric_cols, key="desc_col")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Mean", f"{df[sel_col].mean():.2f}", "📊")
        with c2:
            metric_card("Median", f"{df[sel_col].median():.2f}", "📏")
        with c3:
            metric_card("Std Dev", f"{df[sel_col].std():.2f}", "📐")
        with c4:
            metric_card("Variance", f"{df[sel_col].var():.2f}", "🔢")
    else:
        info_box("No numeric columns found in your dataset.", "warning")

    # Categorical summary
    if cat_cols:
        st.markdown("---")
        st.markdown("##### Categorical Column Summary")
        cat_summary = []
        for col in cat_cols:
            cat_summary.append({
                "Column": col,
                "Unique": df[col].nunique(),
                "Top Value": df[col].mode().iloc[0] if not df[col].mode().empty else "—",
                "Top Frequency": int(df[col].value_counts().iloc[0]) if not df[col].empty else 0,
                "Missing": int(df[col].isna().sum()),
            })
        st.dataframe(pd.DataFrame(cat_summary), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════
# Tab 2: Correlation Matrix
# ══════════════════════════════════════════
with tab_corr:
    st.markdown("##### Correlation Matrix")

    if len(numeric_cols) >= 2:
        method = st.selectbox("Correlation Method", ["pearson", "spearman", "kendall"])
        sel_corr_cols = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:6])

        if len(sel_corr_cols) >= 2:
            corr_matrix = df[sel_corr_cols].corr(method=method)
            fig = px.imshow(
                corr_matrix, text_auto=".2f",
                color_continuous_scale="RdBu_r",
                title=f"{method.capitalize()} Correlation Matrix",
                aspect="auto",
            )
            fig.update_layout(template=DARK_TEMPLATE, height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Strong correlations
            st.markdown("##### 🔍 Strong Correlations (|r| > 0.5)")
            pairs = []
            for i in range(len(sel_corr_cols)):
                for j in range(i+1, len(sel_corr_cols)):
                    r = corr_matrix.iloc[i, j]
                    if abs(r) > 0.5:
                        pairs.append({
                            "Column A": sel_corr_cols[i],
                            "Column B": sel_corr_cols[j],
                            "Correlation": round(r, 4),
                            "Strength": "Strong" if abs(r) > 0.7 else "Moderate",
                        })
            if pairs:
                st.dataframe(pd.DataFrame(pairs), use_container_width=True, hide_index=True)
            else:
                info_box("No strong correlations found among selected columns.", "info")
        else:
            info_box("Select at least 2 columns to compute correlations.", "info")
    else:
        info_box("Need at least 2 numeric columns for correlation analysis.", "warning")

# ══════════════════════════════════════════
# Tab 3: Distribution Analysis
# ══════════════════════════════════════════
with tab_dist:
    st.markdown("##### Distribution Analysis")

    if numeric_cols:
        dist_col = st.selectbox("Select column", numeric_cols, key="dist_col")

        d1, d2 = st.columns(2)

        with d1:
            fig_hist = px.histogram(
                df, x=dist_col, nbins=30, marginal="box",
                title=f"Distribution of {dist_col}",
                opacity=0.8,
            )
            fig_hist.update_layout(template=DARK_TEMPLATE, height=400)
            st.plotly_chart(fig_hist, use_container_width=True)

        with d2:
            fig_qq = go.Figure()
            sorted_vals = np.sort(df[dist_col].dropna().values)
            n = len(sorted_vals)
            theoretical = np.linspace(0.5/n, 1 - 0.5/n, n)
            from scipy import stats
            theoretical_q = stats.norm.ppf(theoretical)
            fig_qq.add_trace(go.Scatter(x=theoretical_q, y=sorted_vals,
                                        mode="markers", name="Data",
                                        marker=dict(color="#00D4FF", size=5, opacity=0.6)))
            # Reference line
            fit = np.polyfit(theoretical_q, sorted_vals, 1)
            fig_qq.add_trace(go.Scatter(x=theoretical_q, y=np.polyval(fit, theoretical_q),
                                        mode="lines", name="Reference",
                                        line=dict(color="#FF0080", dash="dash")))
            fig_qq.update_layout(template=DARK_TEMPLATE, height=400,
                                 title=f"Q-Q Plot: {dist_col}",
                                 xaxis_title="Theoretical Quantiles",
                                 yaxis_title="Sample Quantiles")
            st.plotly_chart(fig_qq, use_container_width=True)

        # Normality test
        if len(df[dist_col].dropna()) >= 8:
            from scipy.stats import shapiro
            stat, p_val = shapiro(df[dist_col].dropna().values[:5000])
            result = "✅ Likely Normal" if p_val > 0.05 else "❌ Not Normal"
            st.markdown(f"**Shapiro-Wilk Test:** W = {stat:.4f}, p = {p_val:.6f} → {result}")
    else:
        info_box("No numeric columns available.", "warning")

# ══════════════════════════════════════════
# Tab 4: Hypothesis Tests
# ══════════════════════════════════════════
with tab_hypo:
    st.markdown("##### Hypothesis Testing")

    from scipy import stats

    test_type = st.selectbox("Test Type", [
        "Independent T-Test (2 columns)",
        "One-Sample T-Test",
        "Chi-Square Test (2 categorical)",
    ])

    if test_type == "Independent T-Test (2 columns)":
        if len(numeric_cols) >= 2:
            tcol1 = st.selectbox("Group A", numeric_cols, key="tcol1")
            tcol2 = st.selectbox("Group B", numeric_cols, key="tcol2", index=min(1, len(numeric_cols)-1))
            alpha = st.number_input("Significance level (α)", 0.001, 0.2, 0.05)

            if st.button("Run T-Test"):
                a = df[tcol1].dropna()
                b = df[tcol2].dropna()
                t_stat, p_val = stats.ttest_ind(a, b)
                result = "Reject H₀ (significant difference)" if p_val < alpha else "Fail to reject H₀"
                st.markdown(f"**t-statistic:** {t_stat:.4f}")
                st.markdown(f"**p-value:** {p_val:.6f}")
                st.markdown(f"**Result (α={alpha}):** {result}")
        else:
            info_box("Need at least 2 numeric columns.", "warning")

    elif test_type == "One-Sample T-Test":
        if numeric_cols:
            os_col = st.selectbox("Column", numeric_cols, key="os_col")
            pop_mean = st.number_input("Population mean (H₀)", value=float(df[numeric_cols[0]].mean()))
            if st.button("Run One-Sample T-Test"):
                t_stat, p_val = stats.ttest_1samp(df[os_col].dropna(), pop_mean)
                result = "Reject H₀" if p_val < 0.05 else "Fail to reject H₀"
                st.markdown(f"**t-statistic:** {t_stat:.4f}")
                st.markdown(f"**p-value:** {p_val:.6f}")
                st.markdown(f"**Result:** {result}")

    elif test_type == "Chi-Square Test (2 categorical)":
        if len(cat_cols) >= 2:
            chi_col1 = st.selectbox("Variable 1", cat_cols, key="chi1")
            chi_col2 = st.selectbox("Variable 2", cat_cols, key="chi2", index=min(1, len(cat_cols)-1))
            if st.button("Run Chi-Square Test"):
                ct = pd.crosstab(df[chi_col1], df[chi_col2])
                chi2, p_val, dof, expected = stats.chi2_contingency(ct)
                result = "Reject H₀ (variables are associated)" if p_val < 0.05 else "Fail to reject H₀"
                st.markdown(f"**χ² statistic:** {chi2:.4f}")
                st.markdown(f"**p-value:** {p_val:.6f}")
                st.markdown(f"**Degrees of freedom:** {dof}")
                st.markdown(f"**Result:** {result}")
                st.markdown("**Contingency Table:**")
                st.dataframe(ct, use_container_width=True)
        else:
            info_box("Need at least 2 categorical columns.", "warning")

# ══════════════════════════════════════════
# Tab 5: Missing Data
# ══════════════════════════════════════════
with tab_missing:
    st.markdown("##### Missing Data Analysis")

    missing_data = df.isna().sum()
    missing_pct = (df.isna().sum() / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing_data.values,
        "Missing %": missing_pct.values,
        "Present Count": (len(df) - missing_data).values,
    }).sort_values("Missing Count", ascending=False)

    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    # Bar chart
    cols_with_missing = missing_df[missing_df["Missing Count"] > 0]
    if not cols_with_missing.empty:
        fig_miss = px.bar(
            cols_with_missing, x="Column", y="Missing %",
            title="Missing Data Percentage by Column",
            color="Missing %", color_continuous_scale=["#00D4FF", "#FF0080"],
        )
        fig_miss.update_layout(template=DARK_TEMPLATE, height=400)
        st.plotly_chart(fig_miss, use_container_width=True)
    else:
        info_box("🎉 No missing data found in your dataset!", "success")

    # Missing pattern heatmap
    if cols_with_missing is not None and not cols_with_missing.empty:
        st.markdown("##### Missing Data Pattern (first 100 rows)")
        pattern = df.head(100).isna().astype(int)
        fig_pattern = px.imshow(
            pattern.T, color_continuous_scale=["#111827", "#FF0080"],
            title="Missing Data Pattern",
            aspect="auto", labels=dict(x="Row", y="Column"),
        )
        fig_pattern.update_layout(template=DARK_TEMPLATE, height=350)
        st.plotly_chart(fig_pattern, use_container_width=True)

# ══════════════════════════════════════════
# Tab 6: Outlier Detection
# ══════════════════════════════════════════
with tab_outlier:
    st.markdown("##### Outlier Detection (IQR Method)")

    if numeric_cols:
        out_col = st.selectbox("Select column", numeric_cols, key="outlier_col")
        iqr_mult = st.slider("IQR Multiplier", 1.0, 3.0, 1.5, 0.1)

        col_data = df[out_col].dropna()
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - iqr_mult * IQR
        upper = Q3 + iqr_mult * IQR
        outliers = df[(df[out_col] < lower) | (df[out_col] > upper)]

        o1, o2, o3, o4 = st.columns(4)
        with o1:
            metric_card("Q1", f"{Q1:.2f}", "📉")
        with o2:
            metric_card("Q3", f"{Q3:.2f}", "📈")
        with o3:
            metric_card("IQR", f"{IQR:.2f}", "📏")
        with o4:
            metric_card("Outliers", f"{len(outliers)}", "🎯")

        st.markdown(f"**Bounds:** [{lower:.2f}, {upper:.2f}]")

        # Box plot with outliers highlighted
        fig_out = go.Figure()
        fig_out.add_trace(go.Box(y=col_data, name=out_col, marker_color="#00D4FF",
                                  boxpoints="outliers"))
        fig_out.update_layout(template=DARK_TEMPLATE, height=400,
                              title=f"Box Plot with Outliers: {out_col}")
        st.plotly_chart(fig_out, use_container_width=True)

        if not outliers.empty:
            st.markdown(f"##### Outlier Rows ({len(outliers)} found)")
            st.dataframe(outliers, use_container_width=True, height=300)
        else:
            info_box("No outliers detected with current IQR multiplier.", "success")
    else:
        info_box("No numeric columns available.", "warning")
