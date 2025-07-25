import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Display logo
try:
    logo = Image.open("images.jpeg")  # Ensure the image is in the same directory
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

# ------------------ 📊 Performance Over Time -------------------
plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()

try:
    plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
    plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
    plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
except Exception as e:
    st.warning("⚠️ Date parsing issue in chart.")

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

# ------------------ 🆚 Compare Two Branches (TOTAL Only) -------------------

st.subheader("🆚 Compare Two Branches (Total Only)")

branches_to_compare = st.multiselect("Choose two branches to compare:", unique_branches, default=unique_branches[:2])

if len(branches_to_compare) == 2:
    branch1, branch2 = branches_to_compare

    df_total = df.copy()
    df_total[df.columns[2]] = df_total[df.columns[2]].astype(str)
    total_data = df_total[df_total[df.columns[2]] == "Total"]

    branch1_data = total_data[total_data[first_col] == branch1]
    branch2_data = total_data[total_data[first_col] == branch2]

    subs1 = set(branch1_data[second_col].dropna().unique())
    subs2 = set(branch2_data[second_col].dropna().unique())
    common_subs = list(subs1.intersection(subs2))

    if not common_subs:
        st.warning("⚠️ No common sub-categories between selected branches.")
    else:
        selected_common_subs = st.multiselect("Choose common sub-categories to compare:", common_subs, default=common_subs[:5])

        if selected_common_subs:
            compare_df = pd.DataFrame(columns=["Sub-category", f"{branch1} On-Time", f"{branch2} On-Time",
                                               f"{branch1} Sign Rate", f"{branch2} Sign Rate"])

            for sub in selected_common_subs:
                row1 = branch1_data[branch1_data[second_col] == sub]
                row2 = branch2_data[branch2_data[second_col] == sub]

                if not row1.empty and not row2.empty:
                    compare_df = pd.concat([compare_df, pd.DataFrame({
                        "Sub-category": [sub],
                        f"{branch1} On-Time": [row1.iloc[0, 4]],
                        f"{branch2} On-Time": [row2.iloc[0, 4]],
                        f"{branch1} Sign Rate": [row1.iloc[0, 5]],
                        f"{branch2} Sign Rate": [row2.iloc[0, 5]],
                    })], ignore_index=True)

            st.subheader("📊 Branch Comparison (Total)")

            fig, ax = plt.subplots(figsize=(12, 6))
            bar_width = 0.35
            x = range(len(compare_df))

            ax.bar([i - bar_width for i in x], compare_df[f"{branch1} On-Time"] * 100, width=bar_width, label=f"{branch1} On-Time", color='green')
            ax.bar([i for i in x], compare_df[f"{branch2} On-Time"] * 100, width=bar_width, label=f"{branch2} On-Time", color='lightgreen')

            ax.bar([i - bar_width for i in x], compare_df[f"{branch1} Sign Rate"] * 100, width=bar_width, bottom=compare_df[f"{branch1} On-Time"] * 100,
                   label=f"{branch1} Sign Rate", color='blue', alpha=0.5)
            ax.bar([i for i in x], compare_df[f"{branch2} Sign Rate"] * 100, width=bar_width, bottom=compare_df[f"{branch2} On-Time"] * 100,
                   label=f"{branch2} Sign Rate", color='skyblue', alpha=0.5)

            ax.set_xticks(x)
            ax.set_xticklabels(compare_df["Sub-category"], rotation=45)
            ax.set_ylabel("Percentage (%)")
            ax.set_title("Comparison of Total On-Time & Sign Rate")
            ax.legend()
            ax.grid(True, axis='y')

            st.pyplot(fig)
