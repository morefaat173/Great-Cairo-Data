import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Logo
try:
    logo = Image.open("images.jpeg")
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ Logo not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load Data
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

# 🧮 Final filtered data
final_result = filtered_df[filtered_df[second_col] == selected_sub].copy()

# 🗓️ Format date column
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]
    def format_date(val):
        try:
            return pd.to_datetime(val).date()
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
    thead tr th {text-align: center !important;}
    tbody tr td {text-align: center !important; font-weight: bold !important;}
    .dataframe-container {font-size: 18px !important;}
    </style>
""", unsafe_allow_html=True)

# 📈 Show table
st.subheader("📈 Branch Data")
st.dataframe(final_result, use_container_width=True)

# ---------------- 🆚 Compare Two Sub-categories on Selected Date ----------------
st.subheader("🆚 Compare Two Sub-categories")

compare_df = df.copy()
compare_df[compare_df.columns[2]] = pd.to_datetime(compare_df[compare_df.columns[2]], errors='coerce')
compare_df[compare_df.columns[2]] = compare_df[compare_df.columns[2]].dt.date

subcats = df[second_col].dropna().unique()
sub1 = st.selectbox("Sub-category 1", subcats, key="sub1")
sub2 = st.selectbox("Sub-category 2", subcats, key="sub2")

# ✅ Available Dates + "Total"
available_dates = compare_df[compare_df[second_col].isin([sub1, sub2])][compare_df.columns[2]].dropna().unique()
available_dates = sorted(available_dates.tolist()) + ["Total"]
chosen_date = st.selectbox("Select Date", available_dates)

# ✅ Select Comparison Type
compare_type = st.radio("Select Comparison Type", ["Both", "On-Time only", "Sign Rate only"], horizontal=True)

# 🔍 Filter data
if chosen_date == "Total":
    filtered_comparison = df[
        (df[second_col].isin([sub1, sub2])) &
        (df[df.columns[2]] == "Total")
    ]
else:
    filtered_comparison = compare_df[
        (compare_df[second_col].isin([sub1, sub2])) &
        (compare_df[compare_df.columns[2]] == chosen_date)
    ]

if not filtered_comparison.empty:
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    categories = filtered_comparison[second_col].tolist()
    x = range(len(categories))
    bar_width = 0.35

    if compare_type in ["Both", "On-Time only"]:
        ontime_vals = filtered_comparison[filtered_comparison.columns[4]].values * 100
        ax.bar([i - bar_width/2 for i in x], ontime_vals, width=bar_width, label="On-Time (%)", color='#8B0000')
        for i in x:
            ax.text(i - bar_width/2, ontime_vals[i] + 1, f"{ontime_vals[i]:.0f}%", ha='center', fontsize=9, color='white')

    if compare_type in ["Both", "Sign Rate only"]:
        sign_vals = filtered_comparison[filtered_comparison.columns[5]].values * 100
        ax.bar([i + bar_width/2 for i in x], sign_vals, width=bar_width, label="Sign Rate (%)", color='#5A0000')
        for i in x:
            ax.text(i + bar_width/2, sign_vals[i] + 1, f"{sign_vals[i]:.0f}%", ha='center', fontsize=9, color='white')

    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='white')
    ax.set_ylabel("Percentage (%)", color='white')
    ax.set_title(f"Comparison on {chosen_date}", color='white')
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax.grid(True, axis='y', alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    st.pyplot(fig)
else:
    st.warning("⚠️ No data found for selected sub-categories and date.")
