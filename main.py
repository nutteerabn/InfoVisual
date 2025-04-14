import cv2
from PIL import Image
import streamlit as st
import numpy as np
from utils import load_gaze_data_from_folder

st.title("🎯 Gaze Point Overlay on Video")

# 🧠 เลือกวิดีโอ
clip_name = st.selectbox("เลือกวิดีโอ", ["APPAL_2a"])

# 👁‍🗨 เลือกเฟรม
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, 700, 0)

# 🎬 โหลดวิดีโอ
video_path = f"Clips (small size)/{clip_name}_c.mp4"
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if not ret:
    st.error("โหลดวิดีโอไม่สำเร็จ")
else:
    h, w, _ = frame.shape

    # 🔄 โหลดข้อมูล gaze
    folder_path = f"clips_folder/{clip_name}"
    gaze_data = load_gaze_data_from_folder(folder_path)

    # 🔴 วาดจุดการมอง
    for viewer in gaze_data:
        frame_indices = (viewer['t'] / 1000 * fps).astype(int)
        idx = np.where(frame_indices == frame_number)[0]

        for i in idx:
            x = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
            y = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

    # 🖼 แสดงภาพพร้อมจุด
    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
