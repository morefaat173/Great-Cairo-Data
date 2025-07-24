import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# إعداد الصفحة
st.set_page_config(page_title="Cairo & Giza Data Analysis", layout="wide")

# عرض الصورة والشعار
col1, col2 = st.columns([1, 8])
with col1:
    try:
        logo = Image.open("images.jpeg")
        st.image(logo, width=80)
    except FileNotFoundError:
        st.warning("Logo not found!")

with col2:
    st.title("📊 Cairo & Giza Data Analysis")

# ----------------------------
# تحميل البيانات من ملف Excel
try:
    df = pd.read_excel("Cairo_Giza_Data.xlsx")
    st.subheader("📂 Excel File: Cairo_Giza_Data.xlsx")
    st.dataframe(df, use_container_width=True)

    st.write("**Data Shape:**", df.shape)
    st.write("**Column Names:**", df.columns.tolist())
    st.write("**Summary Statistics:**")
    st.write(df.describe())
except FileNotFoundError:
    st.error("❌ Cairo_Giza_Data.xlsx file not found.")

# ----------------------------
# تحميل البيانات من ملف CSV
try:
    df_csv = pd.read_csv("Book1(1).csv")
    st.subheader("📂 CSV File: Book1(1).csv")
    st.dataframe(df_csv, use_container_width=True)

    st.write("**Data Shape:**", df_csv.shape)
    st.write("**Column Names:**", df_csv.columns.tolist())
    st.write("**Summary Statistics:**")
    st.write(df_csv.describe())
except FileNotFoundError:
    st.error("❌ Book1(1).csv file not found.")

# ----------------------------
# رسم بياني تفاعلي (لو في أعمدة رقمية)
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist() if 'df' in locals() else []

if numeric_cols:
    st.subheader("📈 Visualize Numeric Column (from Excel data)")
    selected_col = st.selectbox("Select a column to visualize", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_col], kde=True, ax=ax)
    st.pyplot(fig)
else:
    st.warning("No numeric columns found for plotting.")
