import streamlit as st
from utils import download_video_from_drive
import os

# 📦 วิดีโอใน Google Drive (ใช้ File ID)
video_files = {
    "APPAL_2a": "1hJXZmnYPEWjCVBapWU2QRKBvOTt3yqzo",
    "Cloud_17a": "1rehRu2sIywGqHFfypJOl-F7FD34bwxK_"
}

# 📌 สร้างโฟลเดอร์เก็บวิดีโอที่โหลดมา
if not os.path.exists("videos"):
    os.makedirs("videos")

st.title("🎥 Video Player with Slider Control")

# 🔽 dropdown
selected = st.selectbox("เลือกวิดีโอ", list(video_files.keys()))
file_id = video_files[selected]
video_path = f"videos/{selected}.mp4"

# 📥 ดาวน์โหลดถ้ายังไม่มี
if not os.path.exists(video_path):
    with st.spinner("📥 กำลังดาวน์โหลดวิดีโอ..."):
        download_video_from_drive(file_id, video_path)

# 🎬 แสดงวิดีโอ
st.video(video_path)

# (Optional) 🎚 Slider สำหรับเวลา (แต่ Streamlit ยังไม่สามารถ sync ได้ตรงๆ กับวิดีโอ)
