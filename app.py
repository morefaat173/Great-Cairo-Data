# ------------------ 📊 مقارنة بين فرعين -------------------
st.subheader("📊 مقارنة بين فرعين")

# اختيار الفرعين
selected_branches = st.multiselect("اختر فرعين للمقارنة:", unique_branches, default=unique_branches[:2])

# اختيار نوع المؤشر
metric_option = st.radio("اختر نوع المؤشر:", ("On-Time sign", "Sign Rate", "الاثنين معًا"))

if len(selected_branches) == 2:
    compare_df = df[df[first_col].isin(selected_branches)].copy()

    # معالجة التواريخ
    try:
        compare_df[compare_df.columns[2]] = pd.to_datetime(compare_df[compare_df.columns[2]], errors='coerce')
        compare_df = compare_df.dropna(subset=[compare_df.columns[2]])
        compare_df["Date"] = compare_df[compare_df.columns[2]].dt.date
    except:
        st.warning("⚠️ مشكلة في التاريخ أثناء المقارنة.")

    # حذف القيم الناقصة
    compare_df = compare_df.dropna(subset=[compare_df.columns[4], compare_df.columns[5]])

    # إعادة تسمية الأعمدة لتوضيحها
    compare_df.rename(columns={
        compare_df.columns[4]: "On-Time sign",
        compare_df.columns[5]: "Sign Rate",
        first_col: "Branch"
    }, inplace=True)

    # رسم الرسم البياني
    fig2, ax2 = plt.subplots(figsize=(10, 5))

    for branch in selected_branches:
        branch_data = compare_df[compare_df["Branch"] == branch].sort_values(by="Date")

        if metric_option in ["On-Time sign", "الاثنين معًا"]:
            ax2.plot(branch_data["Date"], branch_data["On-Time sign"] * 100,
                     marker='o', label=f"{branch} - On-Time")

        if metric_option in ["Sign Rate", "الاثنين معًا"]:
            ax2.plot(branch_data["Date"], branch_data["Sign Rate"] * 100,
                     marker='s', label=f"{branch} - Sign Rate")

    ax2.set_title("مقارنة المؤشرات بين فرعين")
    ax2.set_xlabel("التاريخ")
    ax2.set_ylabel("النسبة المئوية (%)")
    ax2.legend()
    ax2.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.info("ℹ️ يرجى اختيار فرعين للمقارنة.")
