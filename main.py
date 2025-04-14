import cv2
from PIL import Image
import streamlit as st
import numpy as np
from utils import load_gaze_data_from_folder

# สมมติว่ามี dropdown ให้เลือกวิดีโอ
clip_name = st.selectbox("เลือกวิดีโอ", ["APPAL_2a"])
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, 700, 0)

# โหลดวิดีโอ
video_path = f"Clips (small size)/{clip_name}_c.mp4"
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if ret:
    h, w, _ = frame.shape

    # โหลด gaze data
    folder_path = f"clips_folder/{clip_name}"
    gaze_data = load_gaze_data_from_folder(folder_path)

    for viewer in gaze_data:
        indices = (viewer['t'] / 1000 * 25).astype(int)  # assuming 25 FPS
        idx = np.where(indices == frame_number)[0]
        for i in idx:
            gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
            gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
            cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)

    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
else:
    st.error("โหลดวิดีโอไม่สำเร็จ")
