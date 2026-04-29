"""
Data handler utilities for the Data Analysis Toolkit.
Provides cached data loading, session state helpers, and file parsing.
"""

import streamlit as st
import pandas as pd
import os

SAMPLE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data", "sample.csv")


@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


@st.cache_data
def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file, engine="openpyxl")


def load_file(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith((".xlsx", ".xls")):
        return load_excel(uploaded_file)
    return load_csv(uploaded_file)


def load_sample_data() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_DATA_PATH)


def store_data(df: pd.DataFrame):
    st.session_state["toolkit_data"] = df
    st.session_state["toolkit_data_loaded"] = True


def get_data():
    return st.session_state.get("toolkit_data", None)


def is_data_loaded() -> bool:
    return st.session_state.get("toolkit_data_loaded", False)


def get_numeric_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=["number"]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def get_memory_usage(df: pd.DataFrame) -> str:
    mem = df.memory_usage(deep=True).sum()
    if mem < 1024:
        return f"{mem} B"
    elif mem < 1024 ** 2:
        return f"{mem / 1024:.1f} KB"
    return f"{mem / (1024 ** 2):.2f} MB"


def get_missing_percentage(df: pd.DataFrame) -> float:
    total = df.size
    missing = df.isna().sum().sum()
    return round((missing / total) * 100, 2) if total > 0 else 0.0
