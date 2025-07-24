import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Display logo
try:
    logo = Image.open("images.jpeg")  # تأكد أن الصورة في نفس مجلد app.py
    st.image(logo, width=200)
except FileNotFoundError:
    st.warning("⚠️ Logo image not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load the Excel file
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

# 🗓️ Format date column (column index 2)
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]
    def format_date(val):
        try:
            return pd.to_datetime(val).date()
        except:
            return "Total"
    final_result[date_col] = final_result[date_col].apply(format_date)

# 📊 Format 5th and 6th columns as percentages
for col_index in [4, 5]:
    if final_result.shape[1] > col_index:
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) and isinstance(x, (int, float)) else x
        )

# 🎨 Apply CSS styling for center alignment & bold text
st.markdown("""
    <style>
    thead tr th {text-align: center !important;}
    tbody tr td {text-align: center !important; font-weight: bold !important;}
    .dataframe-container {font-size: 18px !important;}
    </style>
""", unsafe_allow_html=True)

# 📈 Show final table
st.subheader("📈 Branch Data")
st.dataframe(final_result, use_container_width=True)

# ------------------ 📊 CHART COMPARISON -------------------
# Prepare raw data for plotting
plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()

# Convert date column (index 2)
try:
    plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
    plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
    plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
except Exception as e:
    st.warning("⚠️ Date parsing issue in chart.")

# Drop rows with NaN in the percentage columns
plot_df = plot_df.dropna(subset=[plot_df.columns[4], plot_df.columns[5]])

# Sort by date
plot_df = plot_df.sort_values(by=plot_df.columns[2])

# Draw the comparison chart
st.subheader("📊 Performance Comparison Over Time")

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(plot_df[plot_df.columns[2]], plot_df[plot_df.columns[4]] * 100,
        marker='o', label='On-Time sign (%)', color='green')

ax.plot(plot_df[plot_df.columns[2]], plot_df[plot_df.columns[5]] * 100,
        marker='s', label='Sign Rate (%)', color='blue')

ax.set_title(f"{selected_sub} - On-Time vs Sign Rate")
ax.set_xlabel("Date")
ax.set_ylabel("Percentage (%)")
ax.legend()
ax.grid(True)
plt.xticks(rotation=45)

st.pyplot(fig)
