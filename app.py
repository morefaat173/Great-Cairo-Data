import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Great Cairo Delivery", layout="wide")

# 🎾️ Logo and title text
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

# 💕 Load Data
df = pd.read_excel("on.xlsx")
first_col = df.columns[0]
second_col = df.columns[1]

# معالجة التاريخ واستخراج التاريخ فقط
df[df.columns[2]] = pd.to_datetime(df[df.columns[2]], errors='coerce')
df["DateOnly"] = df[df.columns[2]].dt.date

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
            dt = pd.to_datetime(val)
            return dt.strftime('%Y-%m-%d')
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

# 📊 Show table
st.subheader("📊 Branch Data")
st.dataframe(final_result, use_container_width=True)

# --------------------- Compare All Shared Sub-categories Across Branches ----------------------
st.subheader("🔄 Compare Shared Sub-categories (Total)")

if st.button("📌 Show Total Rows by Branch"):
    df_raw = pd.read_excel("on.xlsx")
    total_rows = df_raw[df_raw[df_raw.columns[2]].astype(str).str.strip().str.lower() == "total"]

    if not total_rows.empty:
        available_branches = sorted(total_rows[total_rows.columns[0]].dropna().unique())
        selected_branches = st.multiselect("📌 اختر الفروع لعرض صفوف 'Total':", available_branches)

        if selected_branches:
            filtered_total_rows = total_rows[total_rows[total_rows.columns[0]].isin(selected_branches)]
        else:
            filtered_total_rows = pd.DataFrame()

        if not filtered_total_rows.empty:
            st.markdown("### ✅ نتائج صفوف Total للفروع المحددة")
            st.dataframe(filtered_total_rows, use_container_width=True)
        else:
            st.warning("⚠️ لا توجد صفوف تحتوي على 'Total' للفروع المختارة.")
    else:
        st.warning("⚠️ لا توجد صفوف تحتوي على 'Total' في البيانات.")

# --------------------- Flexible Sub-category Comparison Button ----------------------
with st.expander("📊 Flexible Sub-category Comparison"):
    subcategories_to_compare = st.multiselect("Select Sub-categories:", sorted(df[second_col].dropna().unique()))

    metric_options = {
        "Receivable Amount": df.columns[3],
        "On-Time": df.columns[4],
        "Sign Rate": df.columns[5]
    }
    metric_choices = st.multiselect("Choose Metrics to Compare:", list(metric_options.keys()))

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

                if metric_choice != "Receivable Amount":
                    st.dataframe(pivot_df.reset_index().style.format({metric_col: "{:.0f}"}))
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
    ontime = plot_df[plot_df.columns[4]] * 100
    signrate = plot_df[plot_df.columns[5]] * 100
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
