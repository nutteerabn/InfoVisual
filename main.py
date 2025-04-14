import streamlit as st
import cv2
import os
import numpy as np
import scipy.io
from PIL import Image
from utils import load_gaze_data_from_folder, draw_hulls_on_frame

# 🔧 Page config
st.set_page_config(page_title="Gaze Overlay Viewer", layout="centered")
st.title("🎯 Gaze Overlay on Video with Convex & Concave Hulls")

# 📂 Video options
clip_options = ["APPAL_2a"]
clip_name = st.selectbox("เลือกวิดีโอ", clip_options)

# 🎥 Load video
video_path = f"Clips (small size)/{clip_name}_c.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    st.error("ไม่สามารถโหลดวิดีโอได้")
    st.stop()

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 👁‍🗨 Load gaze data
gaze_data = load_gaze_data_from_folder(f"clips_folder/{clip_name}")

# 🔢 Frame state
if "frame_number" not in st.session_state:
    st.session_state.frame_number = 0

col1, col_spacer, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("Back"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 50)
with col3:
    if st.button("Next"):
        st.session_state.frame_number = min(total_frames - 1, st.session_state.frame_number + 50)

frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, total_frames - 1, st.session_state.frame_number, key="slider")
st.session_state.frame_number = frame_number

# 🖼️ Read current frame
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if not ret:
    st.error("ไม่สามารถโหลดเฟรมวิดีโอได้")
    st.stop()

# 🎯 Plot gaze points on frame
gaze_points_in_frame = []
for viewer in gaze_data:
    indices = (viewer['t'] / 1000 * fps).astype(int)
    idx = np.where(np.abs(indices - frame_number) <= 1)[0]
    for i in idx:
        gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
        gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
        gaze_points_in_frame.append((gx, gy))
        cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)

# 🔵🔴 Draw convex & concave hull
frame = draw_hulls_on_frame(frame, gaze_points_in_frame, alpha=0.03)

# 📷 Show frame
st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
