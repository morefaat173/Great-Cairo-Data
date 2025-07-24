import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ عرض اللوجو
try:
    logo = Image.open("images.jpeg")
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ Logo image not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 تحميل ملف الإكسل
df = pd.read_excel("on.xlsx")

first_col = df.columns[0]
second_col = df.columns[1]
date_col = df.columns[2]
on_time_col = df.columns[4]
sign_rate_col = df.columns[5]

branches = df[first_col].dropna().unique()
categories = df[second_col].dropna().unique()

# 🔘 اختيار الفرعين للمقارنة
st.sidebar.header("🔍 Compare Two Branches")
branch1 = st.sidebar.selectbox("Select First Branch", branches, key="branch1")
branch2 = st.sidebar.selectbox("Select Second Branch", branches, key="branch2")

# 🔘 اختيار نفس التصنيف للفرعين
common_category = st.sidebar.selectbox("Select Sub-category", categories)

# 🔍 تصفية البيانات للفرعين
def prepare_branch_data(branch):
    sub_df = df[(df[first_col] == branch) & (df[second_col] == common_category)].copy()
    sub_df[date_col] = pd.to_datetime(sub_df[date_col], errors='coerce')
    sub_df = sub_df.dropna(subset=[date_col, on_time_col, sign_rate_col])
    sub_df[date_col] = sub_df[date_col].dt.date
    sub_df[on_time_col] = pd.to_numeric(sub_df[on_time_col], errors='coerce')
    sub_df[sign_rate_col] = pd.to_numeric(sub_df[sign_rate_col], errors='coerce')
    return sub_df.sort_values(by=date_col)

branch1_df = prepare_branch_data(branch1)
branch2_df = prepare_branch_data(branch2)

# 📊 رسم المقارنة بين الفرعين
st.subheader(f"📊 Comparison: {branch1} vs {branch2} ({common_category})")

fig, ax = plt.subplots(figsize=(12, 6))

# فرع 1
ax.plot(branch1_df[date_col], branch1_df[on_time_col] * 100,
        label=f'{branch1} - On-Time', marker='o', linestyle='-')
ax.plot(branch1_df[date_col], branch1_df[sign_rate_col] * 100,
        label=f'{branch1} - Sign Rate', marker='x', linestyle='--')

# فرع 2
ax.plot(branch2_df[date_col], branch2_df[on_time_col] * 100,
        label=f'{branch2} - On-Time', marker='o', linestyle='-', color='green')
ax.plot(branch2_df[date_col], branch2_df[sign_rate_col] * 100,
        label=f'{branch2} - Sign Rate', marker='x', linestyle='--', color='orange')

ax.set_title("📈 On-Time Sign & Sign Rate Comparison")
ax.set_xlabel("Date")
ax.set_ylabel("Percentage (%)")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)
