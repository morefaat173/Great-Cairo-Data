import streamlit as st
import pandas as pd

st.set_page_config(page_title="Branch Data Viewer", layout="wide")

st.title("🏢 Branch Data Viewer")

# Load Excel file
try:
    df = pd.read_excel("on.xlsx")
    st.success("✅ File 'on.xlsx' loaded successfully.")
except FileNotFoundError:
    st.error("❌ File 'on.xlsx' not found.")
    st.stop()

# Display all data
st.subheader("📋 Full Dataset")
st.dataframe(df, use_container_width=True)

# Extract branch names from the first column
branch_column = df.columns[0]  # First column
branches = df[branch_column].dropna().unique().tolist()

st.subheader("🔘 Select a Branch to View Its Data")

# Create buttons for each branch
cols = st.columns(3)  # Split buttons into 3 columns
for i, branch in enumerate(branches):
    if cols[i % 3].button(str(branch)):
        st.markdown(f"### 📍 Branch: `{branch}`")
        branch_data = df[df[branch_column] == branch]
        st.table(branch_data.T)  # Display transposed for readability
