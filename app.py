import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import os
from pathlib import Path

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🏎️ Logo and title text with brand colors + shadow
try:
    logo = Image.open("images.jpeg")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(logo, width=200)
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-top: 10px;'>
            <h1 style='
                color: #ED3237;
                font-size: 60px;
                font-weight: bold;
                line-height: 65px;
                margin: 0;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            '>J&amp;T Express Egypt</h1>
            <h2 style='
                color: #ED3237;
                font-size: 40px;
                font-weight: bold;
                margin: 0;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            '>Great Cairo RG</h2>
        </div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Logo not found.")

# 💕 Load Data
df = pd.read_excel("on.xlsx")
first_col = df.columns[0]
second_col = df.columns[1]

df[df.columns[2]] = pd.to_datetime(df[df.columns[2]], errors='coerce')
unique_branches = df[first_col].dropna().unique()

# 🔘 Area selection
selected_branch = st.selectbox("Choose area:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

# 🔘 Branch selection
second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a branch:", second_options)

# 📂 Final filtered data
final_result = filtered_df[filtered_df[second_col] == selected_sub].copy()

# 🗓️ Format date column
if final_result.shape[1] > 2:
    date_col = final_result.columns[2]
    final_result[date_col] = final_result[date_col].apply(
        lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else "Total"
    )

# ✅ Format column 4 as numbers, and 5–6 as percentages
if final_result.shape[1] > 3:
    fourth_col = final_result.columns[3]
    final_result[fourth_col] = pd.to_numeric(final_result[fourth_col], errors='coerce').fillna(0).round(2)

if final_result.shape[1] > 4:
    fifth_col = final_result.columns[4]
    def format_percent(val):
        try:
            num = float(val)
            if num > 1:
                num /= 100
            return f"{num * 100:.0f}%"
        except:
            return val
    final_result[fifth_col] = final_result[fifth_col].apply(format_percent)

if final_result.shape[1] > 5:
    sixth_col = final_result.columns[5]
    final_result[sixth_col] = final_result[sixth_col].apply(
        lambda x: f"{float(x) * 100:.0f}%" if pd.notnull(x) and str(x).replace('.', '', 1).isdigit() else x
    )

# 📂 Show table
st.markdown("""
    <style>
    thead tr th {text-align: center !important; color: white; background-color: #8B0000;}
    tbody tr td {text-align: center !important; font-weight: bold !important; color: white; background-color: #5A0000;}
    .dataframe-container {font-size: 18px !important; background-color: transparent;}
    </style>
""", unsafe_allow_html=True)

st.subheader("📊 Branch Data")
final_result = final_result.drop(columns=["DateOnly"], errors="ignore")
st.dataframe(final_result, use_container_width=True)

# --------------------- Compare All Shared Sub-categories Across Branches ----------------------
# --------------------- Compare All Shared Sub-categories Across Branches ----------------------
st.subheader("🌐 Aggregated Comparison of Area Branches")

if "show_total_rows" not in st.session_state:
    st.session_state.show_total_rows = False

if st.button("🔹Area"):
    st.session_state.show_total_rows = True

if st.session_state.show_total_rows:
    df_raw = pd.read_excel("on.xlsx")

    # ✅ FIXED ERROR HERE
    total_rows = df_raw[df_raw[df_raw.columns[2]].astype(str).str.strip().str.lower() == "total"]

    if not total_rows.empty:
        available_branches = sorted(total_rows[total_rows.columns[0]].dropna().unique())
        selected_branches = st.multiselect("📌 Select Area:", available_branches, key="area_total_selector")

        if selected_branches:
            filtered_total_rows = total_rows[total_rows[total_rows.columns[0]].isin(selected_branches)].copy()

            # Format Receivable Amount
            if filtered_total_rows.shape[1] > 3:
                fourth_col = filtered_total_rows.columns[3]
                filtered_total_rows[fourth_col] = pd.to_numeric(filtered_total_rows[fourth_col], errors='coerce').fillna(0).round(2)

            # Format On-Time & Sign Rate
            for col_index in [-2, -1]:
                if filtered_total_rows.shape[1] > abs(col_index):
                    col_name = filtered_total_rows.columns[col_index]
                    def format_percent(val):
                        try:
                            num = float(val)
                            if num > 1:
                                num /= 100
                            return f"{num * 100:.0f}%"
                        except:
                            return val
                    filtered_total_rows[col_name] = filtered_total_rows[col_name].apply(format_percent)

            st.markdown("###📈 Branch Statistics Comparison")
            st.dataframe(filtered_total_rows, use_container_width=True)
        else:
            st.info("ℹ️ Please select a branch from the list to show data.")
    else:
        st.warning("⚠️ No rows containing 'Total' found in the data.")
# --------------------- Flexible Sub-category Comparison Button ----------------------
with st.expander("📊 Branch Performance Comparison"):
    subcategories_to_compare = st.multiselect("Select Sub-categories:", sorted(df[second_col].dropna().unique()))
    metric_options = {
        "Receivable Amount": df.columns[3],
        "On-Time": df.columns[4],
        "Sign Rate": df.columns[5]
    }
    metric_choices = st.multiselect("Choose Metrics to Compare:", list(metric_options.keys()))
    df["DateOnly"] = df[df.columns[2]].dt.date
    unique_dates = df["DateOnly"].dropna().unique()
    selected_dates = st.multiselect("Select Dates for Comparison:", sorted(unique_dates))

    if subcategories_to_compare and metric_choices and selected_dates:
        comparison_df = df[
            df[second_col].isin(subcategories_to_compare) &
            (df["DateOnly"].isin(selected_dates))
        ]

        for metric_choice in metric_choices:
            metric_col = metric_options[metric_choice]
            if not comparison_df.empty:
                st.markdown(f"### 📌 {metric_choice} Comparison by Date")

                pivot_df = comparison_df.pivot_table(
                    index=[second_col, "DateOnly"],
                    values=metric_col,
                    aggfunc="mean"
                ).fillna(0)

                if metric_choice != "Receivable Amount":
                    pivot_df *= 100
                    st.dataframe(pivot_df.reset_index().style.format({metric_col: "{:.0f}%"}))
                else:
                    st.dataframe(pivot_df.reset_index().style.format({metric_col: "{:.2f}"}))

                st.markdown(":bar_chart: Chart View")
                fig, ax = plt.subplots(figsize=(12, 6))
                pivot_df.unstack().plot(kind='bar', ax=ax, color=['#8B0000', '#5A0000'])
                ax.set_title(f"{metric_choice} by Sub-category and Date", color='white')
                ax.set_xlabel("Sub-category & Date", color='white')
                ax.set_ylabel("%" if metric_choice != "Receivable Amount" else "Amount", color='white')
                ax.tick_params(axis='x', labelrotation=45, colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.legend(loc='best', facecolor='black', labelcolor='white')
                ax.grid(False)
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)
                st.pyplot(fig)
            else:
                st.warning("No matching data found for selected filters.")

# --------------------- Performance Over Time Button ----------------------
if st.button("📊 Branch Performance Comparison"):
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
    ontime = pd.to_numeric(plot_df[plot_df.columns[4]], errors="coerce") * 100
    signrate = pd.to_numeric(plot_df[plot_df.columns[5]], errors="coerce") * 100
    bar_width = 0.4
    x = range(len(dates))

    ax.bar([i - bar_width/2 for i in x], ontime, width=bar_width, label='On-Time', color='#8B0000')
    ax.bar([i + bar_width/2 for i in x], signrate, width=bar_width, label='Sign Rate', color='#5A0000')

    for i in x:
        ax.text(i - bar_width/2, ontime.iloc[i] + 1, f"{ontime.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')
        ax.text(i + bar_width/2, signrate.iloc[i] + 1, f"{signrate.iloc[i]:.0f}%", ha='center', fontsize=8, color='white')

    ax.set_xticks(x)
    ax.set_xticklabels(dates, rotation=45, color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Percentage (%)", color='white')
    ax.set_title(f"{selected_sub} - On-Time & Sign Rate", color='white')
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    ax.grid(False)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    st.pyplot(fig)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Great Cairo Dashboard", layout="wide")

# 📂 Load the Excel files
loss_df = pd.read_excel("疑似遗失Details35914420250727113730.xlsx")
track_df = pd.read_excel("Track real-time monitoring(Details)35914420250727133830.xlsx")

# 🧩 Tabs Layout
tab1, tab2, tab3 = st.tabs(["🅿 Potential Loss", "📌 Track real-time", "🖼️ Daily Report Image"])

# ---------------------------- TAB 1: Suspected Loss ---------------------------- #
with tab1:

    # Summary Pivot Table (Always Visible)
    st.subheader("Summary 2025-08-12 09:50:46")
    summary_pivot = loss_df.pivot_table(index="Resp. BR", columns="Lost type", aggfunc="size", fill_value=0)
    summary_pivot["Total"] = summary_pivot.sum(axis=1)
    summary_pivot = summary_pivot.sort_values("Total", ascending=False)
    st.dataframe(summary_pivot)

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        branches = st.multiselect("Select Branch (Resp. BR):", options=loss_df["Resp. BR"].dropna().unique())
    with col2:
        lost_types = st.multiselect("Select Loss Type:", options=loss_df["Lost type"].dropna().unique())

    # Filtered Data
    filtered_df = loss_df.copy()
    if branches:
        filtered_df = filtered_df[filtered_df["Resp. BR"].isin(branches)]
    if lost_types:
        filtered_df = filtered_df[filtered_df["Lost type"].isin(lost_types)]

    # Table
    st.subheader("📋 Branch Data")
    st.dataframe(filtered_df)

    # Download
    output = BytesIO()
    filtered_df.to_excel(output, index=False, engine='openpyxl')
    st.download_button("⬇ Download Filtered Data", data=output.getvalue(), file_name="filtered_data.xlsx")

    # Full Plot (not filtered)
    st.subheader("📊 Lost type comparison")
    plot_counts = loss_df.groupby(["Resp. BR", "Lost type"]).size().unstack(fill_value=0)
    plot_counts["Total"] = plot_counts.sum(axis=1)
    plot_counts = plot_counts[plot_counts["Total"] > 0].sort_values("Total", ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')
    bar_width = 0.4
    branches_list = plot_counts.index.tolist()
    x = range(len(branches_list))
    selected_types = loss_df["Lost type"].dropna().unique()
    colors = ['#8B0000', '#A52A2A', '#B22222', '#CD5C5C', '#DC143C']

    for i, loss_type in enumerate(selected_types):
        if loss_type in plot_counts.columns:
            values = plot_counts[loss_type]
            positions = [pos + (i - 0.5) * bar_width for pos in x]
            bars = ax.barh(positions, values, height=bar_width, label=loss_type, color=colors[i % len(colors)])
            for bar in bars:
                width = bar.get_width()
                if width > 0:
                    ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f'{int(width)}',
                            va='center', ha='left', color='white', fontsize=8)

    ax.set_yticks(x)
    ax.set_yticklabels(branches_list, color='white')
    ax.set_xlabel("Count", color='white')
    ax.set_title("Loss Types Count per Branch (All Data)", color='white', fontsize=14)
    ax.tick_params(axis='x', colors='white')
    ax.legend(facecolor='black', edgecolor='white', labelcolor='white')
    st.pyplot(fig)

# ---------------------------- TAB 2: Potential Loss ---------------------------- #
with tab2:
    st.header("📌 Track real-time")

    # Pivot Table (Always Visible)
    st.subheader("📊 Track real-time 2025-08-12 09:50:46")
    pivot_summary = track_df.pivot_table(index="latest operator station`s name",
                                         columns="Timeout type",
                                         values="Waybill",
                                         aggfunc="count",
                                         fill_value=0)
    pivot_summary["Total Lost Types"] = pivot_summary.sum(axis=1)
    pivot_summary = pivot_summary.sort_values("Total Lost Types", ascending=False)
    st.dataframe(pivot_summary)

    # Expandable: Branch Filter + Raw Data Table + Download
    with st.expander("🔍 View Full Raw Data & Download by Branch"):
        branch_filter = st.multiselect("Select Branch :",
                                       options=track_df["latest operator station`s name"].dropna().unique())

        df_filtered = track_df.copy()
        if branch_filter:
            df_filtered = df_filtered[df_filtered["latest operator station`s name"].isin(branch_filter)]

        st.dataframe(df_filtered)

        raw_output = BytesIO()
        df_filtered.to_excel(raw_output, index=False, engine='openpyxl')
        st.download_button("⬇ Download Filtered Raw Data", data=raw_output.getvalue(), file_name="filtered_raw_data.xlsx")
from datetime import datetime
from PIL import Image
import os

with tab3:
    st.header("🖼️ Daily Report Image Viewer")

    # Region selector
    region = st.radio("Select Region:", ["Cairo", "Giza"], horizontal=True)

    # Day selector
    selected_day = st.selectbox("Select Day:", list(range(1, 32)))

    # Get current month to use in filename
    today = datetime.now()
    formatted_day = f"{selected_day}-{today.month}"  # e.g. "6-7"

    # Build the expected image filename
    image_name = f"{formatted_day} {region}.jpg"
    image_path = image_name  # ✅ Image is in the same directory as app.py

    # Display the image if found
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=f"Daily Report - {region} ({formatted_day})", use_container_width=True)
    else:
        st.warning(f"⚠️ No image found for {region} on {formatted_day}. Expected: {image_name}")





