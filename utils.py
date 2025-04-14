import os
import scipy.io
import numpy as np

# 🔄 โหลดข้อมูลการมองจากโฟลเดอร์ .mat

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
