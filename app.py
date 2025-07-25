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

# 📅 Load Data
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

# 🧲 Final filtered data
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
    thead tr th {text-align: center !important; color: white; background-color: #8B0000;}
    tbody tr td {text-align: center !important; font-weight: bold !important; color: white; background-color: #5A0000;}
    .dataframe-container {font-size: 18px !important; background-color: transparent;}
    </style>
""", unsafe_allow_html=True)

# 📈 Show table
st.subheader("📈 Branch Data")
st.dataframe(final_result, use_container_width=True)

# --------------------- 📊 PERFORMANCE OVER TIME ----------------------
plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()

try:
    plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
    plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
    plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
except Exception as e:
    st.warning("⚠️ Date parsing error.")

plot_df = plot_df.dropna(subset=[plot_df.columns[4], plot_df.columns[5]])
plot_df = plot_df.sort_values(by=plot_df.columns[2])

# 📊 Bar Chart - On-Time vs Sign Rate Over Time
st.subheader("📊 Performance Over Time")

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_alpha(0)
ax.patch.set_alpha(0)

dates = plot_df[plot_df.columns[2]]
ontime = plot_df[plot_df.columns[4]] * 100
signrate = plot_df[plot_df.columns[5]] * 100
bar_width = 0.4
x = range(len(dates))

ax.bar([i - bar_width/2 for i in x], ontime, width=bar_width, label='On-Time (%)', color='#8B0000')
ax.bar([i + bar_width/2 for i in x], signrate, width=bar_width, label='Sign Rate (%)', color='#5A0000')

for i in x:
    ax.text(i - bar_width/2, ontime.iloc[i] + 1, f"{ontime.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')
    ax.text(i + bar_width/2, signrate.iloc[i] + 1, f"{signrate.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')

ax.set_xticks(x)
ax.set_xticklabels(dates, rotation=45, color='white')
ax.set_xlabel("Date", color='white')
ax.set_ylabel("Percentage (%)", color='white')
ax.set_title(f"{selected_sub} - On-Time vs Sign Rate", color='white')
ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
ax.grid(True, axis='y', alpha=0.2)
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

st.pyplot(fig)

# ------------------ 🤚 Compare Two Sub-categories at Specific Date ------------------
st.subheader("🤚 Compare Two Sub-categories on Selected Date")

# Filter non-total rows with valid dates
compare_df = df.copy()
compare_df[compare_df.columns[2]] = pd.to_datetime(compare_df[compare_df.columns[2]], errors='coerce')
compare_df[compare_df.columns[2]] = compare_df[compare_df.columns[2]].dt.date

subcats = df[second_col].dropna().unique()
sub1 = st.selectbox("Sub-category 1", subcats, key="sub1")
sub2 = st.selectbox("Sub-category 2", subcats, key="sub2")

# Add 'Total' to available dates
all_dates = compare_df[compare_df[second_col].isin([sub1, sub2])][compare_df.columns[2]].dropna().unique().tolist()
all_dates.sort()
all_dates.append("Total")
chosen_date = st.selectbox("Select Date", all_dates)

# Select comparison type
compare_type = st.radio("Select Comparison Type", ["Both", "On-Time only", "Sign Rate only"], horizontal=True)

# Filter data by date
if chosen_date == "Total":
    compare_data = df[
        (df[second_col].isin([sub1, sub2])) &
        (df[df.columns[2]] == "Total")
    ]
else:
    compare_data = compare_df[
        (compare_df[second_col].isin([sub1, sub2])) &
        (compare_df[compare_df.columns[2]] == chosen_date)
    ]

if not compare_data.empty:
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    fig2.patch.set_alpha(0)
    ax2.patch.set_alpha(0)

    bar_width = 0.35
    categories = compare_data[second_col].tolist()
    x = range(len(categories))

    if compare_type in ["Both", "On-Time only"]:
        ontime_vals = compare_data[compare_data.columns[4]].values * 100
        ax2.bar([i - bar_width/2 for i in x], ontime_vals, width=bar_width, label="On-Time (%)", color='#8B0000')
        for i in x:
            ax2.text(i - bar_width/2, ontime_vals[i] + 1, f"{ontime_vals[i]:.0f}%", ha='center', fontsize=9, color='white')

    if compare_type in ["Both", "Sign Rate only"]:
        sign_vals = compare_data[compare_data.columns[5]].values * 100
        ax2.bar([i + bar_width/2 for i in x], sign_vals, width=bar_width, label="Sign Rate (%)", color='#5A0000')
        for i in x:
            ax2.text(i + bar_width/2, sign_vals[i] + 1, f"{sign_vals[i]:.0f}%", ha='center', fontsize=9, color='white')

    ax2.set_xticks(x)
    ax2.set_xticklabels(categories, color='white')
    ax2.set_ylabel("Percentage (%)", color='white')
    ax2.set_title(f"Comparison on {chosen_date}", color='white')
    ax2.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    st.pyplot(fig2)
else:
    st.warning("No data found for selected sub-categories and date.")
