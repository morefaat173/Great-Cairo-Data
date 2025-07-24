import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Cairo & Giza Data Analysis", layout="wide")

# --- عنوان مع الشعار ---
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://raw.githubusercontent.com/morefaat173/Great-Cairo-Data/main/J%26T%20Express%20Logo%20(PNG-480p)%20-%20Vector69Com.png" width="60" style="margin-right: 10px;">
        <h1 style="margin: 0;">📊 Great Cairo Data Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# --- تحميل البيانات ---
df = pd.read_excel("Cairo_Giza_Data.xlsx")

# --- عرض البيانات ---
st.subheader("🗂️ Raw Data")
st.dataframe(df)

# --- معلومات عامة ---
st.subheader("ℹ️ Dataset Info")
st.write(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
st.write("Columns:")
st.write(df.columns.tolist())

# --- إحصائيات رقمية ---
st.subheader("📈 Summary Statistics")
st.write(df.describe())

# --- رسم بياني ---
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
if numeric_cols:
    selected_col = st.selectbox("📌 Choose a numeric column to visualize", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_col], kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_col}")
    st.pyplot(fig)
else:
    st.warning("No numeric columns found to plot.")
