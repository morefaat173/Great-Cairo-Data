import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Display logo
try:
    logo = Image.open("images.jpeg")  # Ensure image is in the same directory
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ Logo image not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load Excel file
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

# 🧮 Filtered data
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

# 📊 Format percentage columns
for col_index in [4, 5]:
    if final_result.shape[1] > col_index:
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) and isinstance(x, (int, float)) else x
        )

# 🎨 CSS styling
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

# ------------------ 📊 Performance Over Time (Bar Chart) -------------------
plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()

# Parse dates
try:
    plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
    plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
    plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
except Exception as e:
    st.warning("⚠️ Issue parsing dates for chart.")

# Drop rows with missing percentages
plot_df = plot_df.dropna(subset=[plot_df.columns[4], plot_df.columns[5]])
plot_df = plot_df.sort_values(by=plot_df.columns[2])

# Draw bar chart
st.subheader("📊 Performance Over Time (Bar Chart)")

fig, ax = plt.subplots(figsize=(12, 6))

# Transparent background
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

dates = plot_df[plot_df.columns[2]]
ontime = plot_df[plot_df.columns[4]] * 100
signrate = plot_df[plot_df.columns[5]] * 100
bar_width = 0.4
x = range(len(dates))

# Bars with red color
ax.bar([i - bar_width/2 for i in x], ontime, width=bar_width, label='On-Time (%)', color='red')
ax.bar([i + bar_width/2 for i in x], signrate, width=bar_width, label='Sign Rate (%)', color='darkred')

# White labels on bars
for i in x:
    ax.text(i - bar_width/2, ontime.iloc[i] + 1, f"{ontime.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')
    ax.text(i + bar_width/2, signrate.iloc[i] + 1, f"{signrate.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')

# Customize axes
ax.set_xticks(x)
ax.set_xticklabels(dates, rotation=45)
ax.set_xlabel("Date")
ax.set_ylabel("Percentage (%)")
ax.set_title(f"{selected_sub} - On-Time vs Sign Rate (Bar Chart)")
ax.legend()
ax.grid(True, axis='y')

st.pyplot(fig)
