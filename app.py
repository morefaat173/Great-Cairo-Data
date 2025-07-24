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

# Format 4th column as percentage
if final_result.shape[1] >= 4:
    final_result[final_result.columns[3]] = final_result[final_result.columns[3]].apply(
        lambda x: f"{x:.0f}%" if pd.notnull(x) else ""
    )

st.subheader("🔎 Filtered Result")
st.dataframe(final_result, use_container_width=True)
