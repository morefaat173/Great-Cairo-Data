import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🗾️ Logo and title text
try:
    logo = Image.open("images.jpeg")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(logo, width=200)
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <h1 style='color: #8B0000; font-size: 60px; font-weight: bold; line-height: 65px; margin: 0;'>J&amp;T Express Egypt</h1>
            <h2 style='color: #8B0000; font-size: 40px; font-weight: bold; margin: 0;'>Great Cairo RG</h2>
        </div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Logo not found.")

st.title("📊 Great Cairo Delivery Data")

# 💕 Load Data
df = pd.read_excel("on.xlsx")
first_col = df.columns[0]
second_col = df.columns[1]

unique_branches = df[first_col].dropna().unique()

# 🔘 Branch selection
selected_branch = st.selectbox("Choose a Branch:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

# 🔘 Sub-category selection
second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

# 📂 Final filtered data
final_result = filtered_df[filtered_df[second_col] == selected_sub].copy()

# 🗓️ Format date column
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]
    def format_date(val):
        try:
            dt = pd.to_datetime(val)
            return dt.strftime('%Y-%m-%d')
        except:
            return "Total"
    final_result[date_col] = final_result[date_col].apply(format_date)

# 📊 Format percentages
for col_index in [4, 5]:
    if final_result.shape[1] > col_index:
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) and isinstance(x, (int, float)) else x
        )

# 🎨 Table styling
st.markdown("""
    <style>
    thead tr th {text-align: center !important; color: white; background-color: #8B0000;}
    tbody tr td {text-align: center !important; font-weight: bold !important; color: white; background-color: #5A0000;}
    .dataframe-container {font-size: 18px !important; background-color: transparent;}
    </style>
""", unsafe_allow_html=True)

# 📊 Show table
st.subheader("📊 Branch Data")
st.dataframe(final_result, use_container_width=True)

# --------------------- Compare All Shared Sub-categories Across Branches ----------------------
st.subheader("🔄 Compare Shared Sub-categories (Total)")

# Identify sub-categories that appear in more than one branch
total_data = df[df[df.columns[2]].astype(str).str.strip().str.lower() == "total"]
sub_counts = total_data.groupby(second_col)[first_col].nunique()
shared_subs = sub_counts[sub_counts > 1].index.tolist()

if shared_subs:
    sub_to_compare = st.selectbox("Select a Shared Sub-category:", sorted(shared_subs))
    compare_data = df[
        (df[second_col] == sub_to_compare) &
        (df[df.columns[2]].astype(str).str.strip().str.lower() == "total")
    ]

    cockpit_cols = st.columns(3)

    with cockpit_cols[0]:
        st.markdown("#### 💰 Receivable Amount")
        for _, row in compare_data.iterrows():
            st.markdown(f"<div style='color:white; font-weight:bold'>{row[first_col]} - {row[second_col]}: {row[df.columns[3]]:.2f}</div>", unsafe_allow_html=True)

    with cockpit_cols[1]:
        st.markdown("#### ⏱️ On-Time")
        for _, row in compare_data.iterrows():
            try:
                percentage = float(row[df.columns[4]]) * 100
                st.markdown(f"<div style='color:white; font-weight:bold'>{row[first_col]} - {row[second_col]}: {percentage:.0f}%</div>", unsafe_allow_html=True)
            except:
                pass

    with cockpit_cols[2]:
        st.markdown("#### 🖊️ Sign Rate")
        for _, row in compare_data.iterrows():
            try:
                percentage = float(row[df.columns[5]]) * 100
                st.markdown(f"<div style='color:white; font-weight:bold'>{row[first_col]} - {row[second_col]}: {percentage:.0f}%</div>", unsafe_allow_html=True)
            except:
                pass
else:
    st.info("No shared sub-categories found across multiple branches.")
