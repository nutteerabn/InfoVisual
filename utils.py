import pandas as pd
import numpy as np

def get_convex_concave_data(clip_name):
    # 🔁 ในเวอร์ชันจริงคุณจะโหลด .mat และวิเคราะห์จริง
    # ตัวอย่าง dummy data
    frames = np.arange(0, 100)
    convex = np.random.uniform(300, 500, size=100)
    concave = convex - np.random.uniform(50, 150, size=100)

    df = pd.DataFrame({
        'Frame': frames,
        'Convex Area (Rolling Avg)': convex,
        'Concave Area (Rolling Avg)': concave
    }).set_index('Frame')

    return df
