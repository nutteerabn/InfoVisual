import streamlit as st

st.title("🎬 Gaze Video Viewer Dashboard")

# วิดีโอ (raw GitHub URLs)
video_links = {
    "APPAL_2a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/APPAL_2a_c.mp4",
    "NANN_3a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/NANN_3a_c.mp4"
}

# ความยาววิดีโอ (ประมาณคร่าว ๆ ในวินาที)
video_durations = {
    "APPAL_2a": 60,  # ตัวอย่าง: 60 วินาที
    "NANN_3a": 45
}

# ✅ dropdown เลือกวิดีโอ
selected_video = st.selectbox("เลือกวิดีโอ", list(video_links.keys()))
video_url = video_links[selected_video]
duration = video_durations[selected_video]

# 🎚 slider ควบคุมวิดีโอ (วินาที)
time_selected = st.slider("⏱ เลือกตำแหน่ง (วินาที)", min_value=0, max_value=duration, step=1, value=0)

# 🎥 แสดงวิดีโอจากเวลาที่เลือก
st.subheader(f"วิดีโอ: {selected_video} (เริ่มที่ {time_selected} วินาที)")
st.video(video_url, start_time=time_selected)
