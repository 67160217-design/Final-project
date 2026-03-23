import streamlit as st
import pandas as pd
import joblib

# 1. โหลดโมเดล Pipeline ที่เราเซฟไว้
# ตรวจสอบให้แน่ใจว่าไฟล์ netflix_pipeline_model.pkl อยู่ในโฟลเดอร์เดียวกันกับ app.py
model = joblib.load('netflix_pipeline_model.pkl')

st.set_page_config(page_title="Netflix Watch Time Predictor", page_icon="🎬")

st.title("🎬 Netflix Watch Time Predictor")
st.markdown("แอปพลิเคชันสำหรับพยากรณ์เวลาการรับชม Netflix เฉลี่ยต่อเดือนของผู้ใช้งาน")

st.sidebar.header("📝 กรอกข้อมูลผู้ใช้งาน")

# 2. สร้างฟอร์มรับข้อมูล (UI) ให้ตรงกับ Features ที่เราใช้ Train
# ข้อมูลหมวดหมู่ (Categorical)
gender = st.sidebar.selectbox("เพศ (Gender)", ["Male", "Female", "Other"])
country = st.sidebar.selectbox("ประเทศ (Country)", ["USA", "India", "UK", "Japan", "Brazil", "Germany", "Australia", "Spain", "Canada", "Other"])
subscription_type = st.sidebar.selectbox("ประเภทสมาชิก (Subscription)", ["Basic", "Standard", "Premium"])
payment_method = st.sidebar.selectbox("ช่องทางชำระเงิน (Payment)", ["PayPal", "Credit Card", "Debit Card", "UPI", "Other"])
primary_device = st.sidebar.selectbox("อุปกรณ์หลัก (Device)", ["Smart TV", "Laptop", "Tablet", "Mobile"])
favorite_genre = st.sidebar.selectbox("แนวหนังที่ชอบ (Genre)", ["Action", "Sci-Fi", "Comedy", "Documentary", "Romance", "Thriller", "Horror", "Drama"])
churned = st.sidebar.selectbox("ยกเลิกสมาชิกหรือไม่ (Churned)", ["Yes", "No"])

# ข้อมูลตัวเลข (Numeric)
age = st.sidebar.slider("อายุ (Age)", 18, 100, 30)
account_age_months = st.sidebar.slider("อายุบัญชี (เดือน)", 1, 120, 12)
monthly_fee = st.sidebar.number_input("ค่าบริการรายเดือน (USD)", 7.99, 20.00, 12.99)
devices_used = st.sidebar.slider("จำนวนอุปกรณ์ที่ใช้", 1, 5, 2)
watch_sessions_per_week = st.sidebar.slider("จำนวนครั้งที่ดูต่อสัปดาห์", 0, 30, 5)
binge_watch_sessions = st.sidebar.slider("จำนวนครั้งที่ดูรวดเดียวจบ", 0, 20, 2)
completion_rate = st.sidebar.slider("เปอร์เซ็นต์การดูจบ (%)", 0.0, 100.0, 50.0)
rating_given = st.sidebar.slider("คะแนนรีวิวที่เคยให้เฉลี่ย", 1.0, 5.0, 3.0)
content_interactions = st.sidebar.slider("การโต้ตอบกับคอนเทนต์ (ครั้ง)", 0, 100, 10)
recommendation_click_rate = st.sidebar.slider("อัตราการคลิกเรื่องที่แนะนำ (%)", 0.0, 100.0, 10.0)
days_since_last_login = st.sidebar.slider("จำนวนวันที่ไม่ได้ล็อกอิน", 0, 100, 2)

# 3. เมื่อกดปุ่มทำนาย
if st.button("🚀 ทำนายเวลาการรับชม"):
    # นำข้อมูลจากฟอร์มมาสร้างเป็น DataFrame แบบ 1 แถว
    input_data = pd.DataFrame({
        'age': [age],
        'gender': [gender],
        'country': [country],
        'account_age_months': [account_age_months],
        'subscription_type': [subscription_type],
        'monthly_fee': [monthly_fee],
        'payment_method': [payment_method],
        'primary_device': [primary_device],
        'devices_used': [devices_used],
        'favorite_genre': [favorite_genre],
        'watch_sessions_per_week': [watch_sessions_per_week],
        'binge_watch_sessions': [binge_watch_sessions],
        'completion_rate': [completion_rate],
        'rating_given': [rating_given],
        'content_interactions': [content_interactions],
        'recommendation_click_rate': [recommendation_click_rate],
        'days_since_last_login': [days_since_last_login],
        'churned': [churned]
    })
    
    # ใช้ Pipeline พยากรณ์ (มันจะจัดการ Missing value, One-hot, Scale ให้เอง)
    prediction = model.predict(input_data)[0]
    
    st.success(f"⏳ คาดว่าจะใช้เวลารับชมเฉลี่ย: **{prediction:.2f} นาที/เดือน**")
    st.balloons()