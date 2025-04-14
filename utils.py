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
