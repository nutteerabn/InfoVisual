import streamlit as st

st.title("🎬 Gaze Video Viewer Dashboard")

# วิดีโอ (raw GitHub URLs)
video_links = {
    "APPAL_2a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/APPAL_2a_c.mp4",
    "NANN_3a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/NANN_3a_c.mp4"
}

# Dropdown เลือกวิดีโอ
selected_video = st.selectbox("เลือกวิดีโอ", list(video_links.keys()))

# แสดงวิดีโอ
if selected_video:
    st.subheader(f"วิดีโอ: {selected_video}")
    st.video(video_links[selected_video])  # ✅ ใช้ raw URL
