# تحميل البيانات من ملف Excel
try:
    df = pd.read_excel("Cairo_Giza_Data.xlsx")
    st.subheader("📂 Excel File: Cairo_Giza_Data.xlsx")
    st.dataframe(df, use_container_width=True)

    # st.write("**Data Shape:**", df.shape)
    st.write("**Column Names:**", df.columns.tolist())
except FileNotFoundError:
    st.error("❌ Cairo_Giza_Data.xlsx file not found.")

# تحميل البيانات من ملف CSV
try:
    df_csv = pd.read_csv("Book1(1).csv")
    st.subheader("📂 CSV File: Book1(1).csv")
    st.dataframe(df_csv, use_container_width=True)

    # st.write("**Data Shape:**", df_csv.shape)
    st.write("**Column Names:**", df_csv.columns.tolist())
except FileNotFoundError:
    st.error("❌ Book1(1).csv file not found.")
