import streamlit as st
import pandas as pd
import joblib

# แนะนำให้ตั้งค่าหน้าเว็บก่อนเป็นอันดับแรก
st.set_page_config(page_title="Netflix Watch Time Predictor", page_icon="🎬", layout="wide")

# 1. โหลดโมเดล Pipeline ที่เราเซฟไว้
@st.cache_resource # ใช้ cache เพื่อให้โหลดโมเดลแค่ครั้งเดียวตอนเปิดแอป
def load_model():
    return joblib.load('netflix_pipeline_model.pkl')

model = load_model()

st.title("🎬 Netflix Watch Time Predictor")
st.markdown("แอปพลิเคชันสำหรับพยากรณ์เวลาการรับชม Netflix เฉลี่ยต่อเดือนของผู้ใช้งาน")
st.markdown("---")

st.header("📝 กรอกข้อมูลผู้ใช้งาน")

# ใช้ st.columns แบ่งหน้าจอเป็น 2 ฝั่งเพื่อให้ดูง่ายขึ้น
col1, col2 = st.columns(2)

# ฝั่งซ้าย: ข้อมูลส่วนตัวและแพ็กเกจ
with col1:
    st.subheader("👤 ข้อมูลทั่วไปและสมาชิก")
    gender = st.selectbox("เพศ (Gender)", ["Male", "Female", "Other"])
    age = st.slider("อายุ (Age)", 18, 100, 30)
    country = st.selectbox("ประเทศ (Country)", ["USA", "India", "UK", "Japan", "Brazil", "Germany", "Australia", "Spain", "Canada", "Other"])
    subscription_type = st.selectbox("ประเภทสมาชิก (Subscription)", ["Basic", "Standard", "Premium"])
    monthly_fee = st.number_input("ค่าบริการรายเดือน (USD)", 7.99, 20.00, 12.99)
    payment_method = st.selectbox("ช่องทางชำระเงิน (Payment)", ["PayPal", "Credit Card", "Debit Card", "UPI", "Other"])
    account_age_months = st.slider("อายุบัญชี (เดือน)", 1, 120, 12)
    churned = st.selectbox("ยกเลิกสมาชิกหรือไม่ (Churned)", ["Yes", "No"])

# ฝั่งขวา: ข้อมูลพฤติกรรมการใช้งาน
with col2:
    st.subheader("🍿 พฤติกรรมการรับชม")
    primary_device = st.selectbox("อุปกรณ์หลัก (Device)", ["Smart TV", "Laptop", "Tablet", "Mobile"])
    devices_used = st.slider("จำนวนอุปกรณ์ที่ใช้", 1, 5, 2)
    favorite_genre = st.selectbox("แนวหนังที่ชอบ (Genre)", ["Action", "Sci-Fi", "Comedy", "Documentary", "Romance", "Thriller", "Horror", "Drama"])
    watch_sessions_per_week = st.slider("จำนวนครั้งที่ดูต่อสัปดาห์", 0, 30, 5)
    binge_watch_sessions = st.slider("จำนวนครั้งที่ดูรวดเดียวจบ", 0, 20, 2)
    completion_rate = st.slider("เปอร์เซ็นต์การดูจบ (%)", 0.0, 100.0, 50.0)
    rating_given = st.slider("คะแนนรีวิวที่เคยให้เฉลี่ย", 1.0, 5.0, 3.0)
    content_interactions = st.slider("การโต้ตอบกับคอนเทนต์ (ครั้ง)", 0, 100, 10)
    recommendation_click_rate = st.slider("อัตราการคลิกเรื่องที่แนะนำ (%)", 0.0, 100.0, 10.0)
    days_since_last_login = st.slider("จำนวนวันที่ไม่ได้ล็อกอิน", 0, 100, 2)

st.markdown("---")

# 3. เมื่อกดปุ่มทำนาย
# ใช้ columns จัดให้ปุ่มอยู่ตรงกลาง (สวยงามขึ้น)
_, btn_col, _ = st.columns([1, 2, 1])

if btn_col.button("🚀 ทำนายเวลาการรับชม", use_container_width=True):
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
    
    try:
        # ใช้ Pipeline พยากรณ์
        prediction = model.predict(input_data)[0]
        
        st.success(f"### ⏳ คาดว่าจะใช้เวลารับชมเฉลี่ย: **{prediction:.2f} นาที/เดือน**")
        st.balloons()
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการพยากรณ์ โปรดตรวจสอบข้อมูลและโมเดลของคุณ: {e}")