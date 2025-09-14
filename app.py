import streamlit as st
import pandas as pd

st.set_page_config(page_title="ریز اقلام پارک‌ها", layout="wide")
st.title("📊 تفکیک اقلام زنده و غیر زنده برای پارک‌ها")

uploaded_file = st.file_uploader("📁 فایل اکسل خود را آپلود کنید", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'نام پارک' not in df.columns or 'نوع' not in df.columns:
        st.error("ستون‌های 'نام پارک' و 'نوع' در فایل یافت نشد.")
    else:
        parks = df['نام پارک'].dropna().unique()
        selected_park = st.selectbox("پارک مورد نظر را انتخاب کنید:", parks)

        park_df = df[df['نام پارک'] == selected_park]
        live_items = park_df[park_df['نوع'] == 'زنده']
        non_live_items = park_df[park_df['نوع'] == 'غیر زنده']

        st.subheader("🌿 اقلام زنده")
        st.dataframe(live_items)

        st.subheader("⚙️ اقلام غیر زنده")
        st.dataframe(non_live_items)
