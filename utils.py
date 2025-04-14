import streamlit as st
import cv2
import os
import numpy as np
import scipy.io
from PIL import Image
from utils import load_gaze_data_from_folder, alpha_shape
from scipy.spatial import ConvexHull

st.set_page_config(page_title="Gaze Viewer", layout="centered")
st.title("🎯 Gaze Point Overlay on Video")

clip_options = ["APPAL_2a"]
clip_name = st.selectbox("เลือกวิดีโอ", clip_options)

video_path = f"Clips (small size)/{clip_name}_c.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    st.error("ไม่สามารถโหลดวิดีโอได้")
    st.stop()

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Load gaze data
folder_path = f"clips_folder/{clip_name}"
gaze_data = load_gaze_data_from_folder(folder_path)

# Frame control
if "frame_number" not in st.session_state:
    st.session_state.frame_number = 0

col1, col_spacer, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("\u2b05\ufe0f\nBack"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 50)
with col3:
    if st.button("Next \u27a1\ufe0f"):
        st.session_state.frame_number = min(total_frames - 1, st.session_state.frame_number + 50)

frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, total_frames - 1, st.session_state.frame_number, key="slider")
st.session_state.frame_number = frame_number

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if not ret:
    st.error("ไม่สามารถโหลดเฟรมวิดีโอได้")
    st.stop()

# Collect gaze points for this frame
gaze_points_in_frame = []
for viewer in gaze_data:
    indices = (viewer['t'] / 1000 * fps).astype(int)
    idx = np.where(np.abs(indices - frame_number) <= 1)[0]
    for i in idx:
        gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
        gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
        gaze_points_in_frame.append((gx, gy))
        cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)  # red dot

# Draw convex and concave hulls
points = np.array(gaze_points_in_frame)
points = np.unique(points, axis=0)

if len(points) >= 3:
    try:
        hull = ConvexHull(points)
        hull_pts = points[hull.vertices].reshape((-1, 1, 2))
        cv2.polylines(frame, [hull_pts], isClosed=True, color=(0, 255, 0), thickness=2)  # green
    except Exception:
        pass

    try:
        concave = alpha_shape(points, alpha=0.01)
        if concave and concave.geom_type == 'Polygon':
            exterior = np.array(concave.exterior.coords).astype(np.int32)
            cv2.polylines(frame, [exterior.reshape((-1, 1, 2))], isClosed=True, color=(255, 0, 0), thickness=2)  # blue
    except Exception:
        pass

st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
