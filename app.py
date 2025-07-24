import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Page configuration
st.set_page_config(page_title="Cairo & Giza Data Analysis", layout="wide")

# Load and display logo with title
logo = Image.open("images.jpeg")
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=100)
with col2:
    st.title("📊 Cairo & Giza Data Analysis")

# Load Excel data
try:
    df = pd.read_excel("Cairo_Giza_Data.xlsx")
except FileNotFoundError:
    st.error("❌ File 'Cairo_Giza_Data.xlsx' not found. Please make sure it's uploaded to your repo.")
    st.stop()

# Show all data
st.subheader("📋 Full Dataset")
st.dataframe(df, use_container_width=True)

# Basic info
st.subheader("ℹ️ Dataset Info")
st.write(f"Number of Rows: {df.shape[0]}")
st.write(f"Number of Columns: {df.shape[1]}")
st.write("Column Names:")
st.write(df.columns.tolist())

# Descriptive statistics
st.subheader("📈 Descriptive Statistics")
st.write(df.describe())

# Numeric column selection for plotting
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
if numeric_cols:
    st.subheader("📊 Plot Column Distribution")
    selected_col = st.selectbox("Select a numeric column to plot:", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(df[selected_col], kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_col}")
    st.pyplot(fig)
else:
    st.warning("⚠️ No numeric columns found to plot.")
