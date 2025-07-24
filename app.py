import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Cairo & Giza Data Explorer", layout="wide")

st.title("📊 Cairo & Giza Data Analysis App")

# Load the Excel file
df = pd.read_excel("Cairo_Giza_Data.xlsx")

# Display full dataframe
st.subheader("📄 Full Dataset")
st.dataframe(df, use_container_width=True)

# General information
st.subheader("📌 Dataset Info")
st.write(f"Total Rows: {df.shape[0]}")
st.write(f"Total Columns: {df.shape[1]}")
st.write("Column Names:")
st.write(df.columns.tolist())

# Statistics
st.subheader("📈 Statistical Summary")
st.write(df.describe())

# Numeric column selection
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if numeric_columns:
    st.subheader("📊 Histogram Plot")
    selected_column = st.selectbox("Select a numeric column:", numeric_columns)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_column], kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_column}")
    st.pyplot(fig)
else:
    st.warning("No numeric columns available for plotting.")
