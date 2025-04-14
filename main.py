import streamlit as st
import cv2
import os
import numpy as np
import scipy.io
from PIL import Image
from scipy.spatial import ConvexHull, Delaunay
from shapely.geometry import MultiPoint, LineString, MultiLineString
from shapely.ops import unary_union, polygonize
from utils import load_gaze_data_from_folder
import time

def alpha_shape(points, alpha):
    if len(points) < 4:
        return MultiPoint(points).convex_hull
    try:
        tri = Delaunay(points, qhull_options='QJ')
    except Exception:
        return MultiPoint(points).convex_hull
    edges = set()
    edge_points = []
    for ia, ib, ic in tri.simplices:
        pa, pb, pc = points[ia], points[ib], points[ic]
        a, b, c = np.linalg.norm(pb - pa), np.linalg.norm(pc - pb), np.linalg.norm(pa - pc)
        s = (a + b + c) / 2.0
        area = max(s * (s - a) * (s - b) * (s - c), 0)
        if area == 0:
            continue
        circum_r = a * b * c / (4.0 * np.sqrt(area))
        if circum_r < 1.0 / alpha:
            edges.update([(ia, ib), (ib, ic), (ic, ia)])
    for i, j in edges:
        edge_points.append(LineString([points[i], points[j]]))
    mls = MultiLineString(edge_points)
    return unary_union(list(polygonize(mls)))

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
gaze_data = load_gaze_data_from_folder(f"clips_folder/{clip_name}")

if "frame_number" not in st.session_state:
    st.session_state.frame_number = 0

col1, col_spacer, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("\u2b05\ufe0f\nBack"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 50)
with col3:
    if st.button("Next\n\u27a1\ufe0f"):
        st.session_state.frame_number = min(total_frames - 1, st.session_state.frame_number + 50)

play = st.checkbox("🎥 Play frames (auto advance)", value=False)

frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, total_frames - 1, st.session_state.frame_number, key="slider")
st.session_state.frame_number = frame_number

if play:
    for fn in range(st.session_state.frame_number, total_frames):
        st.session_state.frame_number = fn
        cap.set(cv2.CAP_PROP_POS_FRAMES, fn)
        ret, frame = cap.read()
        if not ret:
            break
        gaze_points = []
        for viewer in gaze_data:
            indices = (viewer['t'] / 1000 * fps).astype(int)
            idx = np.where(np.abs(indices - fn) <= 1)[0]
            for i in idx:
                gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
                gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
                gaze_points.append((gx, gy))
                cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)
        points = np.array(gaze_points)
        points = np.unique(points, axis=0)
        if len(points) >= 3:
            try:
                hull = ConvexHull(points)
                hull_pts = points[hull.vertices].reshape((-1, 1, 2))
                cv2.polylines(frame, [hull_pts], isClosed=True, color=(0, 255, 0), thickness=2)
                concave = alpha_shape(points, alpha=0.007)
                if concave and concave.geom_type == 'Polygon':
                    exterior = np.array(concave.exterior.coords).astype(np.int32)
                    cv2.polylines(frame, [exterior.reshape((-1, 1, 2))], isClosed=True, color=(255, 0, 0), thickness=2)
            except Exception as e:
                st.warning(f"Hull error: {e}")
        st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {fn}")
        time.sleep(0.05)
        st.experimental_rerun()
else:
    cap.set(cv2.CAP_PROP_POS_FRAMES, st.session_state.frame_number)
    ret, frame = cap.read()
    if not ret:
        st.error("ไม่สามารถโหลดเฟรมวิดีโอได้")
        st.stop()
    gaze_points = []
    for viewer in gaze_data:
        indices = (viewer['t'] / 1000 * fps).astype(int)
        idx = np.where(np.abs(indices - st.session_state.frame_number) <= 1)[0]
        for i in idx:
            gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
            gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
            gaze_points.append((gx, gy))
            cv2.circle(frame, (gx, gy), 5, (0, 0, 255), -1)
    points = np.array(gaze_points)
    points = np.unique(points, axis=0)
    if len(points) >= 3:
        try:
            hull = ConvexHull(points)
            hull_pts = points[hull.vertices].reshape((-1, 1, 2))
            cv2.polylines(frame, [hull_pts], isClosed=True, color=(0, 255, 0), thickness=2)
            concave = alpha_shape(points, alpha=0.007)
            if concave and concave.geom_type == 'Polygon':
                exterior = np.array(concave.exterior.coords).astype(np.int32)
                cv2.polylines(frame, [exterior.reshape((-1, 1, 2))], isClosed=True, color=(255, 0, 0), thickness=2)
        except Exception as e:
            st.warning(f"Hull error: {e}")
    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {st.session_state.frame_number}")
