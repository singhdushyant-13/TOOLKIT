<div align="center">

<img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
<img src="https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

# 🔬 Data Analysis Toolkit

**A premium, interactive data analysis suite built with Streamlit and Plotly.**  
Upload your dataset and explore it with powerful visualization, filtering, and statistical analysis tools — all in a sleek dark-themed UI.

</div>

---

## ✨ Features

### 📊 CSV Viewer
- Drag-and-drop upload for **CSV, Excel (xlsx/xls), and TSV** files
- At-a-glance **stats bar** — rows, columns, numeric count, memory usage, missing %
- **Data Preview** tab with a fully interactive scrollable table
- **Filter & Search** tab — text search across all columns, range sliders for numeric columns, multi-select for categorical columns, and one-click sorting
- **Column Inspector** tab — data type, null counts, unique values, and per-column statistics
- Export filtered data as CSV with one click

### 📈 Chart Generator
- **9 chart types** powered by Plotly — Bar, Line, Scatter, Pie, Histogram, Box Plot, Violin, Area, Heatmap
- Full configuration panel — X/Y axis selection, color grouping, size mapping, opacity, and legend toggle
- Custom **dark Plotly theme** with vibrant cyan/purple/magenta color palette
- **Export charts** as interactive HTML or static PNG
- **Side-by-side chart comparison** for quick exploratory analysis

### 🔢 Statistics Calculator
| Tab | What it does |
|-----|-------------|
| 📋 Descriptive | Mean, median, std, min/max, skewness, kurtosis for all numeric columns |
| 🔗 Correlation | Interactive heatmap with Pearson / Spearman / Kendall methods; highlights strong correlations |
| 📊 Distribution | Histogram with marginal box plot, Q-Q plot, Shapiro-Wilk normality test |
| 🧪 Hypothesis Tests | Independent T-test, one-sample T-test, Chi-square test |
| ❓ Missing Data | Missing count & percentage table, bar chart, and row-by-row pattern heatmap |
| 🎯 Outliers | IQR-based outlier detection with adjustable multiplier, box plot, and outlier row table |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/singhdushyant-13/TOOLKIT.git
cd TOOLKIT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** For PNG chart export, also install `kaleido`:
> ```bash
> pip install kaleido
> ```

### 3. Run the app
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
TOOLKIT/
├── app.py                        # 🏠 Home page & entry point
├── requirements.txt              # 📦 Python dependencies
├── pages/
│   ├── 1_📊_CSV_Viewer.py        # CSV upload, filter, export
│   ├── 2_📈_Chart_Generator.py   # Interactive chart builder
│   └── 3_🔢_Statistics.py        # Statistical analysis suite
├── utils/
│   ├── __init__.py
│   ├── theme.py                  # Custom CSS & UI components
│   └── data_handler.py           # Cached data loading & session state
└── sample_data/
    └── sample.csv                # 🧪 Built-in demo dataset (50 rows)
```

---

## 🧪 Sample Dataset

The toolkit ships with a **50-row employee dataset** so you can start exploring immediately without uploading your own data. It includes:

| Column | Type | Description |
|--------|------|-------------|
| Name, Department, City | Categorical | Employee demographics |
| Age, Experience_Years | Numeric | Experience info |
| Salary | Numeric | Annual salary (USD) |
| Performance_Score | Numeric | Score out of 100 |
| Projects_Completed | Numeric | Total completed projects |
| Satisfaction_Rating | Numeric | 1–5 rating |
| Join_Date | Date | Hire date |

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| [Streamlit](https://streamlit.io) | ≥ 1.30 | Web app framework |
| [Plotly](https://plotly.com/python/) | ≥ 5.18 | Interactive visualizations |
| [Pandas](https://pandas.pydata.org) | ≥ 2.0 | Data manipulation |
| [NumPy](https://numpy.org) | ≥ 1.24 | Numerical computing |
| [SciPy](https://scipy.org) | ≥ 1.11 | Statistical tests & distributions |
| [openpyxl](https://openpyxl.readthedocs.io) | ≥ 3.1 | Excel file support |

---

## 🎨 Design

The UI uses a **premium dark theme** with:
- Animated gradient title (cyan → purple → magenta)
- **Glassmorphism** metric cards with gradient top-border accents
- Plotly charts rendered in a custom dark template
- Smooth CSS hover transitions on cards and buttons
- Custom-styled Streamlit components (tabs, file uploader, selects, buttons)
- [Inter](https://rsms.me/inter/) typography via Google Fonts

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">
  Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> + <a href="https://plotly.com">Plotly</a>
</div>
