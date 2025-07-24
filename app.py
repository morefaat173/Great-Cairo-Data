import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cairo & Giza Branch Viewer", layout="wide")

st.title("🏢 Cairo & Giza Branch Viewer")

# تحميل ملف Excel
try:
   df = pd.read_csv("Book1(1).csv")
    st.success("✅ تم تحميل ملف Cairo_Giza_Data.xlsx بنجاح.")
except FileNotFoundError:
    st.error("❌ لم يتم العثور على ملف Excel: Cairo_Giza_Data.xlsx")
    st.stop()

# عرض الجدول الكامل
st.subheader("📄 جميع البيانات")
st.dataframe(df, use_container_width=True)

# --- استخراج أسماء الفروع ---
branch_col = df.columns[0]  # نفترض أن العمود الأول هو اسم الفرع
branches = df[branch_col].dropna().unique().tolist()

st.subheader("🧭 اختر فرعًا لعرض تفاصيله")

# إنشاء أزرار في أعمدة
cols = st.columns(3)  # عدد الأعمدة (يمكن تغييره)

for i, branch in enumerate(branches):
    if cols[i % 3].button(branch):
        st.markdown(f"### 🏷️ تفاصيل الفرع: `{branch}`")
        branch_data = df[df[branch_col] == branch]

        # عرض البيانات بشكل عمودي لتكون أسهل في القراءة
        st.table(branch_data.T)
