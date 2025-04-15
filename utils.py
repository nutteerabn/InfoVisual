import os
import scipy.io
import numpy as np
import cv2
from scipy.spatial import ConvexHull, Delaunay
from shapely.geometry import MultiPoint, LineString, MultiLineString
from shapely.ops import unary_union, polygonize

# โหลด gaze data
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

# ฟังก์ชันสร้าง concave hull
def alpha_shape(points, alpha=0.03):
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
        area = np.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
        if area == 0:
            continue
        circum_r = a * b * c / (4.0 * area)
        if circum_r < 1.0 / alpha:
            edges.update([(ia, ib), (ib, ic), (ic, ia)])

    for i, j in edges:
        edge_points.append(LineString([points[i], points[j]]))

    mls = MultiLineString(edge_points)
    return unary_union(polygonize(mls))

# วาด convex และ concave hull ลงบน frame
def draw_hulls_on_frame(frame, gaze_points, alpha=0.03):
    if len(gaze_points) < 3:
        return frame  # ไม่พอวาด

    points = np.array(gaze_points)
    points = np.unique(points, axis=0)

    # convex
    try:
        hull = ConvexHull(points)
        hull_pts = points[hull.vertices].reshape((-1, 1, 2))
        cv2.polylines(frame, [hull_pts], isClosed=True, color=(0, 0, 255), thickness=2)  # 🔴 Red
    except:
        pass

    # concave
    try:
        concave = alpha_shape(points, alpha=alpha)
        if concave and concave.geom_type == 'Polygon':
            coords = np.array(concave.exterior.coords).astype(np.int32)
            cv2.polylines(frame, [coords.reshape((-1, 1, 2))], isClosed=True, color=(255, 0, 0), thickness=2)  # 🔵 Blue
    except:
        pass

    return frame

####joe

import os
import cv2
import numpy as np
import pandas as pd
import requests
import scipy.io
from io import BytesIO
from scipy.spatial import ConvexHull
import alphashape

def list_mat_files(user, repo, folder):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{folder}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    files = r.json()
    return [f["name"] for f in files if f["name"].endswith(".mat")]

def load_gaze_data(user, repo, folder):
    mat_files = list_mat_files(user, repo, folder)
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

def download_video(video_url, save_path):
    r = requests.get(video_url)
    with open(save_path, "wb") as f:
        f.write(r.content)

def analyze_gaze(gaze_data, video_path, alpha=0.007, window=20):
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

        points = []
        for x, y, t in gaze_data:
            idx = (t / 1000 * fps).astype(int)
            if i in idx:
                pts = np.where(idx == i)[0]
                for p in pts:
                    px = int(np.clip(x[p], 0, 1) * (w - 1))
                    py = int(np.clip(y[p], 0, 1) * (h - 1))
                    points.append((px, py))

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
