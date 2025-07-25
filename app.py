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
    st.warning("⚠️ Logo image not found.")

st.title("📊 Great Cairo Delivery Data")

# 📥 Load Excel
df = pd.read_excel("on.xlsx")

first_col = df.columns[0]
second_col = df.columns[1]

unique_branches = df[first_col].dropna().unique()

# 🔘 Branch selection
selected_branch = st.selectbox("Choose a Branch:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

# 🔘 Sub-category
second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

# 🧮 Filtered result
final_result = filtered_df[filtered_df[second_col] == selected_sub].copy()

# 🗓️ Format date
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]

    def format_date(val):
        try:
            return pd.to_datetime(val).date()
        except:
            return "Total"

    final_result[date_col] = final_result[date_col].apply(format_date)

# 📊 Percent format
for col_index in [4, 5]:
    if final_result.shape[1] > col_index:
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) and isinstance(x, (int, float)) else x
        )

# 🎨 Styling
st.markdown("""
    <style>
    thead tr th {text-align: center !important;}
    tbody tr td {text-align: center !important; font-weight: bold !important;}
    .dataframe-container {font-size: 18px !important;}
    </style>
""", unsafe_allow_html=True)

# 📈 Table
st.subheader("📈 Branch Data")
st.dataframe(final_result, use_container_width=True)

# 📊 Single Branch Chart
plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()
try:
    plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
    plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
    plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
except:
    st.warning("⚠️ Date parsing error.")

plot_df = plot_df.dropna(subset=[plot_df.columns[4], plot_df.columns[5]])
plot_df = plot_df.sort_values(by=plot_df.columns[2])

st.subheader("📊 Performance Over Time")

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

# 🆚 Comparison Section
st.subheader("🆚 Compare Two Branches")

branch_1 = st.selectbox("Select First Branch:", unique_branches, key="branch1")
branch_2 = st.selectbox("Select Second Branch:", unique_branches, key="branch2")

# ✅ Choose metrics to compare
compare_metrics = st.multiselect(
    "Select metrics to compare:",
    ["On-Time sign", "Sign Rate"],
    default=["On-Time sign", "Sign Rate"]
)

# Start plotting
if branch_1 != branch_2 and compare_metrics:
    fig2, ax2 = plt.subplots(figsize=(10, 5))

    for branch, color in zip([branch_1, branch_2], ['orange', 'purple']):
        comp_df = df[(df[first_col] == branch) & (df[second_col] == selected_sub)].copy()
        try:
            comp_df[comp_df.columns[2]] = pd.to_datetime(comp_df[comp_df.columns[2]], errors='coerce')
            comp_df = comp_df.dropna(subset=[comp_df.columns[2], comp_df.columns[4], comp_df.columns[5]])
            comp_df[comp_df.columns[2]] = comp_df[comp_df.columns[2]].dt.date
            comp_df = comp_df.sort_values(by=comp_df.columns[2])

            if "On-Time sign" in compare_metrics:
                ax2.plot(comp_df[comp_df.columns[2]], comp_df[comp_df.columns[4]] * 100,
                         label=f"{branch} - On-Time", linestyle='-', marker='o', color=color)

            if "Sign Rate" in compare_metrics:
                ax2.plot(comp_df[comp_df.columns[2]], comp_df[comp_df.columns[5]] * 100,
                         label=f"{branch} - Sign Rate", linestyle='--', marker='x', color=color)

        except:
            st.warning(f"⚠️ Data issue with branch: {branch}")

    ax2.set_title(f"Comparison Between {branch_1} and {branch_2} - {selected_sub}")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Percentage (%)")
    ax2.legend()
    ax2.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(fig2)
elif branch_1 == branch_2:
    st.info("Please select two **different** branches to compare.")
elif not compare_metrics:
    st.info("Please select **at least one** metric to compare.")
