import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("on.xlsx")

first_col = df.columns[0]
second_col = df.columns[1]

unique_branches = df[first_col].dropna().unique()

st.title("📍 Select Branch and Sub-category")

selected_branch = st.selectbox("Choose a Branch:", unique_branches)
filtered_df = df[df[first_col] == selected_branch]

second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

final_result = filtered_df[filtered_df[second_col] == selected_sub]

# Format the 5th and 6th columns (index 4 and 5) as percentages
for col_index in [4, 5]:
    if final_result.shape[1] > col_index:
        col_name = final_result.columns[col_index]
        final_result[col_name] = final_result[col_name].apply(
            lambda x: f"{x * 100:.0f}%" if pd.notnull(x) else ""
        )

st.subheader("🔎 Filtered Result")
st.dataframe(final_result, use_container_width=True)
