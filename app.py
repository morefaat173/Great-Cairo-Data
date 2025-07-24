import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Display logo
try:
    logo = Image.open("images.jpeg")
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ Logo image not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load data
df = pd.read_excel("on.xlsx")

# Column references
area_col, branch_col, date_col = df.columns[:3]
on_time_col, sign_rate_col = df.columns[4], df.columns[5]

# 🔘 Select two branches for comparison
branches = df[branch_col].dropna().unique()
col1, col2 = st.columns(2)
with col1:
    branch_1 = st.selectbox("🔹 Choose Branch 1:", branches)
with col2:
    branch_2 = st.selectbox("🔸 Choose Branch 2:", branches, index=1 if len(branches) > 1 else 0)

# Filter data
def prepare_branch_data(branch_name):
    temp_df = df[df[branch_col] == branch_name].copy()
    temp_df[date_col] = pd.to_datetime(temp_df[date_col], errors='coerce')
    temp_df = temp_df.dropna(subset=[date_col, on_time_col, sign_rate_col])
    temp_df[date_col] = temp_df[date_col].dt.date
    temp_df = temp_df.sort_values(by=date_col)
    return temp_df

df1 = prepare_branch_data(branch_1)
df2 = prepare_branch_data(branch_2)

# 🧮 Display first branch filtered data
st.subheader(f"📄 Data for {branch_1}")
table_df = df1.copy()

# Format date and percentage
table_df[on_time_col] = table_df[on_time_col].apply(lambda x: f"{x*100:.0f}%" if pd.notnull(x) else "")
table_df[sign_rate_col] = table_df[sign_rate_col].apply(lambda x: f"{x*100:.0f}%" if pd.notnull(x) else "")
table_df[date_col] = table_df[date_col].apply(lambda x: x if isinstance(x, pd.Timestamp) else x)

# Apply style
st.markdown("""
    <style>
    thead tr th {text-align: center !important;}
    tbody tr td {text-align: center !important; font-weight: bold !important;}
    .dataframe-container {font-size: 18px !important;}
    </style>
""", unsafe_allow_html=True)

st.dataframe(table_df, use_container_width=True)

# 📊 Chart comparison
st.subheader("📈 Branch Comparison Over Time")

fig, ax = plt.subplots(figsize=(12, 5))

# Plot for On-Time sign
ax.plot(df1[date_col], df1[on_time_col]*100, label=f"{branch_1} - On-Time", marker='o', color='green')
ax.plot(df2[date_col], df2[on_time_col]*100, label=f"{branch_2} - On-Time", marker='o', linestyle='--', color='green')

# Plot for Sign Rate
ax.plot(df1[date_col], df1[sign_rate_col]*100, label=f"{branch_1} - Sign Rate", marker='s', color='blue')
ax.plot(df2[date_col], df2[sign_rate_col]*100, label=f"{branch_2} - Sign Rate", marker='s', linestyle='--', color='blue')

ax.set_xlabel("Date")
ax.set_ylabel("Percentage (%)")
ax.set_title("Comparison of On-Time Sign and Sign Rate Between Branches")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)
