from pathlib import Path
from PIL import Image
import streamlit as st
import cv2
import numpy as np
import scipy.io
import os

# โหลด gaze data
def load_gaze_data_from_folder(folder_path):
    gaze_data = []
    for mat_file in Path(folder_path).glob("*.mat"):
        data = scipy.io.loadmat(mat_file)
        if "eyetrackRecord" in data:
            record = data["eyetrackRecord"]
            x = record["x"][0][0].flatten()
            y = record["y"][0][0].flatten()
            t = record["t"][0][0].flatten()
            valid = (x != -32768) & (y != -32768)
            gaze_data.append({
                "x": x[valid] / max(x[valid]) if max(x[valid]) else x[valid],
                "y": y[valid] / max(y[valid]) if max(y[valid]) else y[valid],
                "t": t[valid] - t[valid][0]
            })
    return gaze_data

# 📺 Streamlit UI
st.set_page_config(page_title="Gaze Overlay", layout="wide")
st.title("🎯 Gaze Point Overlay on Video")

video_options = {
    "APPAL_2a": "Clips (small size)/APPAL_2a_c.mp4",
    "NANN_3a": "Clips (small size)/NANN_3a_c.mp4"
}
clip_name = st.selectbox("เลือกวิดีโอ", list(video_options.keys()))
video_path = video_options[clip_name]

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
ret, sample_frame = cap.read()
cap.release()

if not ret:
    st.error("ไม่สามารถโหลดวิดีโอได้")
    st.stop()

h, w, _ = sample_frame.shape
max_frame = total_frames - 1

# 🧠 Session state
if "frame_number" not in st.session_state:
    st.session_state.frame_number = 0

# ⏮⏭️ Buttons
col1, col_spacer, col3 = st.columns([1, 8, 1])
with col1:
    if st.button("⏮ Previous"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 20)
with col3:
    if st.button("Next ⏭️"):
        st.session_state.frame_number = min(max_frame, st.session_state.frame_number + 20)

# 🎚️ Slider
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, max_frame, st.session_state.frame_number)
st.session_state.frame_number = frame_number

# 📥 Load gaze
gaze_folder = f"clips_folder/{clip_name}"
gaze_data = load_gaze_data_from_folder(gaze_folder)

cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if ret:
    for viewer in gaze_data:
        indices = (viewer["t"] / 1000 * fps).astype(int)
        idx = np.where(np.abs(indices - frame_number) <= 1)[0]
        for i in idx:
            gx = int(np.clip(viewer["x"][i], 0, 1) * (w - 1))
            gy = int(np.clip(viewer["y"][i], 0, 1) * (h - 1))
            cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)

    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
else:
    st.error("โหลดเฟรมไม่สำเร็จ")
