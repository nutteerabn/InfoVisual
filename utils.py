import pandas as pd
import numpy as np
import gdown

def get_convex_concave_data(clip_name):
    # 🔁 ตัวอย่าง dummy data
    frames = np.arange(0, 100)
    convex = np.random.uniform(300, 500, size=100)
    concave = convex - np.random.uniform(50, 150, size=100)

    df = pd.DataFrame({
        'Frame': frames,
        'Convex Area (Rolling Avg)': convex,
        'Concave Area (Rolling Avg)': concave
    }).set_index('Frame')

    return df

def download_video_from_drive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)

import scipy.io
import numpy as np
import os

def load_gaze_data_from_folder(folder_path):
    gaze_data_per_viewer = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".mat"):
            mat = scipy.io.loadmat(os.path.join(folder_path, filename))
            eyetrack = mat['eyetrackRecord']
            gaze_x = eyetrack['x'][0, 0].flatten()
            gaze_y = eyetrack['y'][0, 0].flatten()
            timestamps = eyetrack['t'][0, 0].flatten()

            valid = (gaze_x != -32768) & (gaze_y != -32768)
            gaze_x = gaze_x[valid]
            gaze_y = gaze_y[valid]
            timestamps = timestamps[valid] - timestamps[0]

            gaze_x_norm = gaze_x / np.max(gaze_x)
            gaze_y_norm = gaze_y / np.max(gaze_y)

            gaze_data_per_viewer.append({
                'viewer': filename,
                'x': gaze_x_norm,
                'y': gaze_y_norm,
                't': timestamps
            })
    return gaze_data_per_viewer

import os
import scipy.io
import numpy as np
import math
from shapely.geometry import MultiPoint, LineString, MultiLineString
from shapely.ops import unary_union, polygonize
from scipy.spatial import ConvexHull, Delaunay

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
        area = math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
        if area == 0:
            continue
        circum_r = a * b * c / (4.0 * area)
        if circum_r < 1.0 / alpha:
            edges.update([(ia, ib), (ib, ic), (ic, ia)])

    for i, j in edges:
        edge_points.append(LineString([points[i], points[j]]))

    mls = MultiLineString(edge_points)
    return unary_union(list(polygonize(mls)))
