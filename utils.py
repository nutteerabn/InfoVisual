import os
import cv2
import numpy as np
import pandas as pd
import requests
import scipy.io
from io import BytesIO
from scipy.spatial import ConvexHull
import alphashape
import streamlit as st

# ✅ ดาวน์โหลดวิดีโอ (มี cache)
@st.cache_resource
def download_video(video_url, save_path):
    if not os.path.exists(save_path):
        r = requests.get(video_url)
        with open(save_path, "wb") as f:
            f.write(r.content)

# ✅ โหลด gaze data พร้อม caching
@st.cache_data(show_spinner="Loading gaze data...")
def load_gaze_data(user, repo, folder):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{folder}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    mat_files = [f["name"] for f in response.json() if f["name"].endswith(".mat")]
    gaze_data = []
    for file in mat_files:
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{folder}/{file}"
        res = requests.get(raw_url)
        if res.status_code == 200:
            mat = scipy.io.loadmat(BytesIO(res.content))
            record = mat['eyetrackRecord']
            x = record['x'][0, 0].flatten()
            y = record['y'][0, 0].flatten()
            t = record['t'][0, 0].flatten()
            valid = (x != -32768) & (y != -32768)
            gaze_data.append({
                'x': x[valid] / np.max(x[valid]),
                'y': y[valid] / np.max(y[valid]),
                't': t[valid] - t[valid][0]
            })
    return [(d['x'], d['y'], d['t']) for d in gaze_data]

# ✅ วิเคราะห์ gaze patterns และคำนวณพื้นที่ hull
@st.cache_data(show_spinner="Analyzing gaze patterns...")
def analyze_gaze(gaze_data, video_path, alpha=0.007, window=20, frame_skip=2):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frames, convex, concave, images = [], [], [], []
    i = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % frame_skip != 0:
            i += 1
            continue

        points = []
        for x, y, t in gaze_data:
            idx = (t / 1000 * fps).astype(int)
            if i in idx:
                pts = np.where(idx == i)[0]
                px = np.clip((x[pts] * (w - 1)).astype(int), 0, w - 1)
                py = np.clip((y[pts] * (h - 1)).astype(int), 0, h - 1)
                points.extend(zip(px, py))

        if len(points) >= 3:
            arr = np.array(points)
            try:
                convex_area = ConvexHull(arr).volume
            except:
                convex_area = 0
            try:
                shape = alphashape.alphashape(arr, alpha)
                concave_area = shape.area if shape.geom_type == 'Polygon' else 0
            except:
                concave_area = 0
        else:
            convex_area = concave_area = 0

        frames.append(i)
        convex.append(convex_area)
        concave.append(concave_area)
        images.append(frame)
        i += 1

    cap.release()

    df = pd.DataFrame({
        'Frame': frames,
        'Convex Area': convex,
        'Concave Area': concave
    }).set_index('Frame')

    df['Convex Area (Rolling)'] = df['Convex Area'].rolling(window, min_periods=1).mean()
    df['Concave Area (Rolling)'] = df['Concave Area'].rolling(window, min_periods=1).mean()
    df['F-C score'] = 1 - (df['Convex Area (Rolling)'] - df['Concave Area (Rolling)']) / df['Convex Area (Rolling)']
    df['F-C score'] = df['F-C score'].fillna(0)

    return df, images
