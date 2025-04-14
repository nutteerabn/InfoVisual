import os
import math
import cv2
import numpy as np
import pandas as pd
import scipy.io
import streamlit as st
import altair as alt
from PIL import Image
from scipy.spatial import ConvexHull, Delaunay
from shapely.geometry import MultiPoint, LineString, MultiLineString
from shapely.ops import unary_union, polygonize

# ==== ฟังก์ชันคำนวณ concave hull =====
def alpha_shape(points, alpha=0.007):
    if len(points) < 4:
        return MultiPoint(points).convex_hull
    try:
        tri = Delaunay(points, qhull_options='QJ')
    except:
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
    return unary_union(polygonize(MultiLineString(edge_points)))

# ==== โหลด gaze data ====
@st.cache_data
def load_gaze_data_from_folder(folder_path):
    gaze_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".mat"):
            data = scipy.io.loadmat(os.path.join(folder_path, filename))
            record = data['eyetrackRecord']
            x = record['x'][0, 0].flatten()
            y = record['y'][0, 0].flatten()
            t = record['t'][0, 0].flatten()
            valid = (x != -32768) & (y != -32768)
            gaze_data.append({
                'x': x[valid] / np.max(x[valid]),
                'y': y[valid] / np.max(y[valid]),
                't': t[valid] - t[valid][0]
            })
    return gaze_data

# ==== เริ่ม Streamlit ====
st.set_page_config(page_title="Gaze Viewer", layout="wide")
st.title("🎯 Gaze Point + Convex vs Concave Dashboard")

clip_name = st.selectbox("เลือกวิดีโอ", ["APPAL_2a"])
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

# ==== แถว 2: วิดีโอ preview ====
st.video(video_path)

# ==== แถว 3: ปุ่ม back / next ====
col1, col_space, col3 = st.columns([1, 6, 1])
with col1:
    if st.button("⬅️ Back"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 10)
with col3:
    if st.button("Next ➡️"):
        st.session_state.frame_number = min(total_frames - 1, st.session_state.frame_number + 10)

# ==== แถว 4: slider เฟรม ====
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, total_frames - 1, st.session_state.frame_number, key="slider")
st.session_state.frame_number = frame_number

cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()
if not ret:
    st.error("โหลดเฟรมวิดีโอไม่สำเร็จ")
    st.stop()

# ==== พล็อตจุดและ hull ====
gaze_points = []
for viewer in gaze_data:
    indices = (viewer['t'] / 1000 * fps).astype(int)
    idx = np.where(np.abs(indices - frame_number) <= 1)[0]
    for i in idx:
        gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
        gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
        gaze_points.append((gx, gy))
        cv2.circle(frame, (gx, gy), 4, (0, 0, 255), -1)

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

# ==== เตรียมข้อมูลกราฟ ====
frame_list = []
convex_list = []
concave_list = []

for f in range(total_frames):
    pts = []
    for viewer in gaze_data:
        indices = (viewer['t'] / 1000 * fps).astype(int)
        idx = np.where(np.abs(indices - f) <= 1)[0]
        for i in idx:
            gx = int(np.clip(viewer['x'][i], 0, 1) * (w - 1))
            gy = int(np.clip(viewer['y'][i], 0, 1) * (h - 1))
            pts.append((gx, gy))
    pts = np.unique(np.array(pts), axis=0)
    if len(pts) >= 3:
        try:
            convex_area = ConvexHull(pts).volume
        except:
            convex_area = 0
        try:
            concave_shape = alpha_shape(pts, alpha=0.007)
            concave_area = concave_shape.area if concave_shape.geom_type == 'Polygon' else 0
        except:
            concave_area = 0
        frame_list.append(f)
        convex_list.append(convex_area)
        concave_list.append(concave_area)

df = pd.DataFrame({
    'Frame': frame_list,
    'Convex Area': convex_list,
    'Concave Area': concave_list
})
df['Convex Area (Rolling Avg)'] = df['Convex Area'].rolling(window=20, min_periods=1).mean()
df['Concave Area (Rolling Avg)'] = df['Concave Area'].rolling(window=20, min_periods=1).mean()
df['Score'] = ((df['Convex Area (Rolling Avg)'] - df['Concave Area (Rolling Avg)']) /
               (df['Convex Area (Rolling Avg)'] + 1e-6)).clip(0, 1)

# ==== แถว 5: แสดงกราฟ + วิดีโอเฟรม + ค่าคะแนน ====
col_graph, col_vis = st.columns([2, 1])

with col_graph:
    df_melt = df.melt(id_vars='Frame', value_vars=[
        'Convex Area (Rolling Avg)', 'Concave Area (Rolling Avg)'],
        var_name='Metric', value_name='Area')
    chart = alt.Chart(df_melt).mark_line().encode(
        x='Frame',
        y='Area',
        color=alt.Color('Metric:N',
                        scale=alt.Scale(domain=['Convex Area (Rolling Avg)', 'Concave Area (Rolling Avg)'],
                                        range=['green', 'blue']))
    ).properties(width=500, height=300)

    rule = alt.Chart(pd.DataFrame({'Frame': [frame_number]})).mark_rule(color='red').encode(x='Frame')
    st.altair_chart(chart + rule, use_container_width=True)

with col_vis:
    st.image(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), caption=f"Frame {frame_number}")
    st.metric("Score", f"{df.loc[frame_number, 'Score']:.3f}")
