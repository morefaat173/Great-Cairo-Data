import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("on.xlsx")

first_col = df.columns[0]
second_col = df.columns[1]

unique_branches = df[first_col].dropna().unique()

st.title("📊 Great Cairo Delivery Data")

# Branch selection
selected_branch = st.selectbox("Choose a Branch:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

# Sub-category selection
second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

# Filtered final result
final_result = filtered_df[filtered_df[second_col] == selected_sub]

# Format 5th and 6th columns as percentage if exist
if final_result.shape[1] >= 6:
    for col_index in [4, 5]:  # columns 5 and 6
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) else ""
        )

# Format 3rd column as date or 'Total'
date_col_index = 2
if final_result.shape[1] > date_col_index:
    col_name = final_result.columns[date_col_index]
    parsed_dates = pd.to_datetime(final_result[col_name], errors='coerce')
    final_result[col_name] = [
        d.date() if pd.notnull(d) else "Total"
        for d in parsed_dates
    ]

# Inject custom CSS for styling the dataframe
st.markdown("""
    <style>
    .dataframe th, .dataframe td {
        text-align: center !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 12px !important;
    }
    .stDataFrame > div {
        max-height: 800px;
    }
    </style>
""", unsafe_allow_html=True)

# Display the final filtered data
st.subheader("📈 Branch Data")
st.dataframe(final_result, use_container_width=True)
