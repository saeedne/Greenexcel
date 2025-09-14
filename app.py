import streamlit as st
import pandas as pd

st.set_page_config(page_title="ریز اقلام پارک‌ها", layout="wide")
st.title("📊 تفکیک اقلام زنده و غیر زنده برای پارک‌ها")

uploaded_file = st.file_uploader("📁 فایل اکسل خود را آپلود کنید", type=["xlsx"])

if uploaded_file:
    try:
        # خواندن فایل با openpyxl
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # نمایش ستون‌های موجود
        st.write("🧾 ستون‌های موجود در فایل:", df.columns.tolist())

        # فقط ستون‌هایی که رشته هستن بررسی می‌شن
        columns = [col for col in df.columns if isinstance(col, str)]
        park_col = next((col for col in columns if 'پارک' in col), None)
        type_col = next((col for col in columns if 'نوع' in col), None)

        if not park_col or not type_col:
            st.error("❌ ستون‌های 'نام پارک' و 'نوع' پیدا نشدند.")
        else:
            parks = df[park_col].dropna().unique()
            selected_park = st.selectbox("🏞️ پارک مورد نظر را انتخاب کنید:", sorted(parks))

            park_df = df[df[park_col] == selected_park]
            live_items = park_df[park_df[type_col] == 'زنده']
            non_live_items = park_df[park_df[type_col] == 'غیر زنده']

            st.subheader("🌿 اقلام زنده")
            if not live_items.empty:
                st.dataframe(live_items)
            else:
                st.info("هیچ قلم زنده‌ای برای این پارک ثبت نشده.")

            st.subheader("⚙️ اقلام غیر زنده")
            if not non_live_items.empty:
                st.dataframe(non_live_items)
            else:
                st.info("هیچ قلم غیر زنده‌ای برای این پارک ثبت نشده.")

            # نمایش تعداد اقلام
            st.markdown(f"✅ مجموع اقلام زنده: **{len(live_items)}**")
            st.markdown(f"✅ مجموع اقلام غیر زنده: **{len(non_live_items)}**")

    except Exception as e:
        st.error(f"❗ خطا در پردازش فایل: {e}")
