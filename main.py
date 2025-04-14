import streamlit as st

# ดิกชันนารีเก็บลิงก์วิดีโอที่ใช้ raw.githubusercontent.com
video_urls = {
    "APPAL_2a": "https://raw.githubusercontent.com/your-username/InfoVisual/main/Clips%20(small%20size)/APPAL_2a_c.mp4",
    "NANN_3a": "https://raw.githubusercontent.com/your-username/InfoVisual/main/Clips%20(small%20size)/NANN_3a_c.mp4"
}

st.title("🎥 Gaze Video Viewer Dashboard")

# ✅ เลือกวิดีโอ
selected = st.selectbox("เลือกวิดีโอ", list(video_urls.keys()))

if selected:
    video_url = video_urls[selected]
    st.subheader(f"วิดีโอ: {selected}")
    st.video(video_url)

    # ✅ เพิ่ม Slider ที่แสดง frame (ยังไม่เชื่อมกับ video player)
    st.slider("⏱️ เลือกตำแหน่ง (Frame)", min_value=0, max_value=500, value=0, step=1)
