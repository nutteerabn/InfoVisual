import streamlit as st
import streamlit.components.v1 as components

# วิดีโอที่ embed จาก Google Drive (แบบ /preview)
video_links = {
    "APPAL_2a": "https://drive.google.com/file/d/14k3dbuZXYMtEP6BNIdN_Wvb4hdK0BFaM/preview",
    "SIMPS_9a": "https://drive.google.com/file/d/1hJXZmnYPEWjCVBapWU2QRKBvOTt3yqzo/preview"
}

st.title("🎬 Eye Gaze Dashboard – GDrive Video")

# Dropdown
selected_clip = st.selectbox("เลือกวิดีโอ", list(video_links.keys()))

# แสดงวิดีโอใน iframe
if selected_clip:
    st.subheader(f"วิดีโอ: {selected_clip}")
    video_url = video_links[selected_clip]
    
    # ใส่ iframe โดยใช้ components
    components.iframe(video_url, height=480, width=800)
