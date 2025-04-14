import streamlit as st
import cv2
from PIL import Image
import numpy as np
from utils import load_gaze_data_from_folder

st.set_page_config(page_title="Gaze Point Viewer", layout="wide")
st.title("🎯 Gaze Point Overlay on Video")

# 🗂 ชื่อคลิปและ path
video_options = {
    "APPAL_2a": {
        "video_path": "Clips (small size)/APPAL_2a_c.mp4",
        "gaze_folder": "clips_folder/APPAL_2a",
        "max_frame": 700
    },
    "NANN_3a": {
        "video_path": "Clips (small size)/NANN_3a_c.mp4",
        "gaze_folder": "clips_folder/NANN_3a",
        "max_frame": 700
    }
}

clip_name = st.selectbox("เลือกวิดีโอ", list(video_options.keys()))
video_path = video_options[clip_name]["video_path"]
gaze_folder = video_options[clip_name]["gaze_folder"]
max_frame = video_options[clip_name]["max_frame"]

# 🎯 กำหนดค่าเริ่มต้น
if 'frame_number' not in st.session_state:
    st.session_state.frame_number = 0

# ⏮▶️ ปุ่มควบคุม
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⏮ Previous"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 1)
with col2:
    if st.button("▶️ Next"):
        st.session_state.frame_number = min(max_frame, st.session_state.frame_number + 1)

# 🔧 แถบเลื่อน
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, max_frame, st.session_state.frame_number)
st.session_state.frame_number = frame_number  # อัปเดต session

# 📥 โหลดวิดีโอเฟรม
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if ret:
    h, w, _ = frame.shape

    # 📍 โหลดข้อมูล gaze
    gaze_data = load_gaze_data_from_folder(gaze_folder)

    fps = 25  # ถ้าไม่ได้อ่านจากวิดีโอจริงให้กำหนดไว้ก่อน
    for viewer in gaze_data:
        indices = (viewer['t'] / 1000 * fps).astype(int)
        idx = np.where(np.abs(indices - frame_number) <= 1)[0]
        for i in idx:
            gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
            gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
            cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)

    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
else:
    st.error("โหลดวิดีโอไม่สำเร็จ")
