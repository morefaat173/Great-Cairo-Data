import streamlit as st
import pandas as pd

# Load the Excel file
df = pd.read_excel("on.xlsx")

# Get unique values from the first column (e.g., Branch names)
first_col = df.columns[0]
second_col = df.columns[1]

unique_branches = df[first_col].dropna().unique()

st.title("📍 Select Branch and Sub-category")

# First level: Buttons for branch names
selected_branch = st.selectbox("Choose a Branch:", unique_branches)

# Filter based on selected branch
filtered_df = df[df[first_col] == selected_branch]

# Second level: Based on second column (e.g., departments)
second_options = filtered_df[second_col].dropna().unique()
selected_sub = st.selectbox("Choose a Sub-category:", second_options)

# Final filter
final_result = filtered_df[filtered_df[second_col] == selected_sub]

st.subheader("🔎 Filtered Result")
st.dataframe(final_result, use_container_width=True)
