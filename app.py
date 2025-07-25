import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🖼️ Logo and title text
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

# 🗕️ Load Data
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

# --------------------- Cockpit Comparison by Total ----------------------
st.subheader("🧙 Branch Comparison Cockpit")

total_rows = df[df[df.columns[2]].astype(str).str.strip() == "Total"].copy()
selected_branches = st.multiselect("Select Branches to Compare:", df[first_col].dropna().unique())

if selected_branches:
    cockpit_cols = st.columns(3)
    filtered_total = total_rows[total_rows[first_col].isin(selected_branches)]

    with cockpit_cols[0]:
        st.markdown("#### Receivable Amount")
        for _, row in filtered_total.iterrows():
            st.markdown(f"**{row[first_col]} - {row[second_col]}:** {row[df.columns[3]]:.2f}")

    with cockpit_cols[1]:
        st.markdown("#### On-Time")
        for _, row in filtered_total.iterrows():
            st.markdown(f"**{row[first_col]} - {row[second_col]}:** {row[df.columns[4]] * 100:.0f}%")

    with cockpit_cols[2]:
        st.markdown("#### Sign Rate")
        for _, row in filtered_total.iterrows():
            st.markdown(f"**{row[first_col]} - {row[second_col]}:** {row[df.columns[5]] * 100:.0f}%")
else:
    st.info("Please select one or more branches to compare.")

# --------------------- Flexible Sub-category Comparison Button ----------------------
if st.button("📊 Flexible Sub-category Comparison"):
    st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <h2 style='color: #8B0000; font-size: 36px; font-weight: bold;'>Flexible Sub-category Comparison</h2>
        </div>
    """, unsafe_allow_html=True)

    subcategories_to_compare = st.multiselect("Select Sub-categories:", sorted(df[second_col].dropna().unique()))

    metric_options = {
        "Receivable Amount": df.columns[3],
        "On-Time": df.columns[4],
        "Sign Rate": df.columns[5]
    }
    metric_choices = st.multiselect("Choose Metrics to Compare:", list(metric_options.keys()))

    if subcategories_to_compare and metric_choices:
        comparison_df = df[
            df[second_col].isin(subcategories_to_compare) &
            (df[df.columns[2]].astype(str).str.strip() == "Total")
        ]

        for metric_choice in metric_choices:
            metric_col = metric_options[metric_choice]
            if not comparison_df.empty:
                st.markdown(f"### 📌 {metric_choice} Comparison")
                pivot_df = comparison_df.pivot(index=second_col, columns=first_col, values=metric_col).fillna(0)

                if metric_choice != "Receivable Amount":
                    pivot_df *= 100

                st.dataframe(pivot_df.style.format("{:.0f}" if metric_choice != "Receivable Amount" else "{:.2f}"))
            else:
                st.warning("No matching data found for selected filters.")

# --------------------- Performance Over Time Button ----------------------
if st.button("📊 Show Performance Over Time"):
    plot_df = filtered_df[filtered_df[second_col] == selected_sub].copy()

    try:
        plot_df[plot_df.columns[2]] = pd.to_datetime(plot_df[plot_df.columns[2]], errors='coerce')
        plot_df = plot_df.dropna(subset=[plot_df.columns[2]])
        plot_df[plot_df.columns[2]] = plot_df[plot_df.columns[2]].dt.date
    except Exception as e:
        st.warning("⚠️ Date parsing error.")

    plot_df = plot_df.dropna(subset=[plot_df.columns[4], plot_df.columns[5]])
    plot_df = plot_df.sort_values(by=plot_df.columns[2])

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
