import streamlit as st

# === วิดีโอจาก Google Drive (แบบ share link) ===
video_links = {
    "APPAL_2a": "https://drive.google.com/file/d/14k3dbuZXYMtEP6BNIdN_Wvb4hdK0BFaM/preview",
    "SIMPS_9a": "https://drive.google.com/file/d/1hJXZmnYPEWjCVBapWU2QRKBvOTt3yqzo/preview",
    # เพิ่มชื่อวิดีโอและลิงก์เพิ่มได้ที่นี่
}

st.title("🎥 Eye Gaze Video Dashboard")

# === Dropdown สำหรับเลือกวิดีโอ ===
selected_clip = st.selectbox("เลือกวิดีโอที่ต้องการดู", list(video_links.keys()))

# === ฝังวิดีโอจาก Google Drive ===
if selected_clip:
    st.subheader(f"วิดีโอ: {selected_clip}")
    st.video(video_links[selected_clip])
