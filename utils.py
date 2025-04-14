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
