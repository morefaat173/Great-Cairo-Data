import streamlit as st
import pandas as pd  # ← ضروري جداً
from PIL import Image

st.set_page_config(page_title="Cairo & Giza Data", layout="wide")
st.title("📊 Cairo & Giza Data Analysis")

# عرض الشعار (لو موجود)
try:
    logo = Image.open("images.jpeg")
    st.image(logo, width=100)
except:
    st.warning("Logo image not found.")

# قراءة ملف Excel
try:
    df = pd.read_excel("Cairo_Giza_Data.xlsx")
    st.subheader("📂 Excel File: Cairo_Giza_Data.xlsx")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error("❌ Cairo_Giza_Data.xlsx file not found.")

# قراءة ملف CSV
try:
    df_csv = pd.read_csv("Book1(1).csv")
    st.subheader("📂 CSV File: Book1(1).csv")
    st.dataframe(df_csv, use_container_width=True)
except FileNotFoundError:
    st.error("❌ Book1(1).csv file not found.")
