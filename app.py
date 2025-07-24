import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Logo
try:
    logo = Image.open("images.jpeg")
    st.image(logo, width=200)
except:
    st.warning("⚠️ Logo not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load Excel
df = pd.read_excel("on.xlsx")

# 🎯 Select Branches for comparison
branches = df["Branch Name"].dropna().unique()
selected_branches = st.multiselect("Choose up to 2 Branches to Compare:", branches, default=branches[:2])

# 🧮 Proceed if 2 branches are selected
if len(selected_branches) == 2:
    comp_df = df[df["Branch Name"].isin(selected_branches)].copy()
    comp_df["Date"] = pd.to_datetime(comp_df["Date"], errors='coerce')
    comp_df = comp_df.dropna(subset=["Date", "On-Time sign", "Sign"])
    comp_df = comp_df.sort_values(by="Date")

    # 📊 Plot comparison
    st.subheader("📈 On-Time Sign vs Sign Rate Comparison")

    fig, ax = plt.subplots(figsize=(12, 6))

    for branch in selected_branches:
        branch_data = comp_df[comp_df["Branch Name"] == branch]
        ax.plot(branch_data["Date"], branch_data["On-Time sign"], label=f"{branch} - On-Time", marker='o')
        ax.plot(branch_data["Date"], branch_data["Sign"], label=f"{branch} - Sign Rate", marker='s')

    ax.set_title("Branch Comparison Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(fig)

# 🔽 Optional: Show raw data
if st.checkbox("Show Raw Data Table"):
    st.dataframe(df, use_container_width=True)
