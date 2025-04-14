import streamlit as st

# วิดีโอ raw URL จาก GitHub
video_urls = {
    "APPAL_2a": "https://raw.githubusercontent.com/your-username/InfoVisual/main/Clips%20(small%20size)/APPAL_2a_c.mov",
    "NANN_3a": "https://raw.githubusercontent.com/your-username/InfoVisual/main/Clips%20(small%20size)/NANN_3a_c.mov"
}

# 🌟 ชื่อคลิป
selected = st.selectbox("เลือกวิดีโอ", list(video_urls.keys()))
video_url = video_urls[selected]

# 🔘 slider ควบคุมตำแหน่งวิดีโอ (เป็นวินาที สมมุติความยาว 60 วินาที)
time = st.slider("เลื่อนเวลา", min_value=0, max_value=60, value=0)

# 🎥 แสดงวิดีโอ
st.video(video_url, start_time=time)
