import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# 🚀 إعداد الصفحة
st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ تحميل اللوجو والعنوان
try:
    logo = Image.open("images.jpeg")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(logo, width=200)
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <h1 style='color: #8B0000; font-size: 60px; font-weight: bold; line-height: 65px; margin: 0;'>J&T Express Egypt</h1>
            <h2 style='color: #8B0000; font-size: 40px; font-weight: bold; margin: 0;'>Great Cairo RG</h2>
        </div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Logo not found.")

st.title("📊 Great Cairo Delivery Data")

# 🧾 تحميل البيانات
df = pd.read_excel("on.xlsx")
first_col = df.columns[0]
second_col = df.columns[1]

# ⏰ تحويل التاريخ
df[df.columns[2]] = pd.to_datetime(df[df.columns[2]], errors='coerce')
df["DateOnly"] = df[df.columns[2]].dt.date

# 🔘 اختيار الفرع والفئة الفرعية
unique_branches = df[first_col].dropna().unique()
selected_branch = st.selectbox("Choose a Branch:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

# 📂 تصفية البيانات النهائية
final_result = filtered_df[filtered_df[second_col] == selected_sub].copy()

# 🗓️ تنسيق التاريخ
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]
    final_result[date_col] = final_result[date_col].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d') if pd.notnull(x) else "Total")

# 🎯 تحويل الأعمدة إلى نسب مئوية (الرابع وقبله اثنين)
percent_columns = [3, -2, -1]
for col_index in percent_columns:
    if final_result.shape[1] > abs(col_index):
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{float(x)/100*100:.0f}%" if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else x
        )

# 🎨 تنسيق جدول العرض
st.markdown("""
    <style>
    thead tr th {text-align: center !important; color: white; background-color: #8B0000;}
    tbody tr td {text-align: center !important; font-weight: bold !important; color: white; background-color: #5A0000;}
    .dataframe-container {font-size: 18px !important; background-color: transparent;}
    </style>
""", unsafe_allow_html=True)

st.subheader("📊 Branch Data")
final_result = final_result.drop(columns=["DateOnly"], errors="ignore")
st.dataframe(final_result, use_container_width=True)
