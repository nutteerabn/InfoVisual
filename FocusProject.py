import os
import cv2
import requests
import altair as alt
import streamlit as st
import pandas as pd
import scipy.io
from io import BytesIO
from scipy.spatial import ConvexHull
import alphashape

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Focus Dashboard", layout="wide")

# -------------------- CSS for Animation --------------------
st.markdown("""
<style>
@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
.popup-section {
    animation: slideUp 1s ease-out forwards;
    opacity: 0;
}
.section-1 { animation-delay: 0.5s; }
.section-2 { animation-delay: 1.5s; }
.section-3 { animation-delay: 2.5s; }
.section-4 { animation-delay: 3.5s; }
</style>
""", unsafe_allow_html=True)

# -------------------- SECTION 1–4: Conceptual Visualization --------------------
st.image("conclip/Image.jpeg", use_container_width=True)

st.markdown("""
<div class="popup-section section-1" style="background-color: #DCEEFF; padding: 25px; border-radius: 10px; margin-top: 30px;">
<blockquote style="font-size: 1.1em; text-align: center; font-weight: bold; font-style: italic; border-left: 6px solid #95A5A6; background-color: #ECF0F1; padding: 1em; margin: 1.5em 0; border-radius: 6px;">
    “Is the viewer’s attention firmly focused on key moments,<br>
    or does it float, drifting between different scenes in search of something new?”
</blockquote>
<p style="font-size: 1.05em;">
    This visualization explores how viewers engage with a video by examining where and how they focus their attention.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="popup-section section-2" style="background-color: #DCEEFF; padding: 25px; border-radius: 10px; margin-top: 30px;">
<h3>📐 How Do We Measure Focus?</h3>
<p style="font-size: 1.05em;">We use geometric shapes to visualize how tightly the viewer’s gaze is grouped:</p>
<ul style="font-size: 1.05em;">
    <li><b>Convex Hull</b>: Encloses all gaze points loosely.</li>
    <li><b>Concave Hull</b>: Follows the actual shape of gaze, revealing true focus.</li>
</ul>
<p style="font-size: 1.05em;">👉 The <b>difference in area</b> between the two tells us how spread out or concentrated the gaze is.</p>
<div style="display: flex; gap: 20px; justify-content: space-between;">
    <div style="width: 48%;">
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_image.jpg" style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; margin-top: 8px;">📊 Diagram: Convex vs Concave Hulls</p>
    </div>
    <div style="width: 48%;">
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_SIMPS_9a.gif" style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; margin-top: 8px;">🎥 Real Example: Gaze Boundaries Over Time</p>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="popup-section section-3" style="background-color:#f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">
<h3>📊 Focus-Concentration (F-C) Score</h3>
<img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/formula_image.jpeg" style="width: 100%; border-radius: 8px;">
<p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic; margin-top: 8px;">🧮 Area calculation using a rolling average across the last 20 frames</p>
<p style="font-size: 1.05em;">
    The <b>F-C Score</b> helps quantify gaze behavior:
</p>
<ul style="font-size: 1.05em;">
    <li><b>Close to 1</b> → tight gaze cluster → <span style="color:#2e7d32;"><b>high concentration</b></span>.</li>
    <li><b>Much lower than 1</b> → scattered gaze → <span style="color:#d32f2f;"><b>low concentration / exploration</b></span>.</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="popup-section section-4" style="background-color: #f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">
<h3>🎥 Visual Examples of Focus</h3>
<div style="display: flex; gap: 20px;">
    <div style="width: 50%;">
        <h4>High F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_high_F-C_score.gif" style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic;">Gaze remains tightly grouped in one region.</p>
    </div>
    <div style="width: 50%;">
        <h4>Low F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_low_F-C_score.gif" style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic;">Gaze jumps around, showing exploration or distraction.</p>
    </div>
</div>
<p style="font-size: 1.05em; margin-top: 1.5em;">You’ll see this visualized dynamically in the graph and overlays as you explore different segments of the video.</p>
</div>
""", unsafe_allow_html=True)

# -------------------- INTERACTIVE ANALYSIS --------------------
st.markdown("---")
st.header("📊 Interactive Analysis")

# Config
video_files = {
    "APPAL_2a": "APPAL_2a_hull_area.mp4",
    "FOODI_2a": "FOODI_2a_hull_area.mp4",
    "MARCH_12a": "MARCH_12a_hull_area.mp4",
    "NANN_3a": "NANN_3a_hull_area.mp4",
    "SHREK_3a": "SHREK_3a_hull_area.mp4",
    "SIMPS_19a": "SIMPS_19a_hull_area.mp4",
    "SIMPS_9a": "SIMPS_9a_hull_area.mp4",
    "SUND_36a_POR": "SUND_36a_POR_hull_area.mp4",
}
base_video_url = "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/processed%20hull%20area%20overlay/"
user = "nutteerabn"
repo = "InfoVisual"
clips_folder = "clips_folder"

@st.cache_data
def list_mat_files(user, repo, folder):
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{folder}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    return [f["name"] for f in r.json() if f["name"].endswith(".mat")]

@st.cache_data
def load_gaze_data(user, repo, folder):
    files = list_mat_files(user, repo, folder)
    data = []
    for f in files:
        url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{folder}/{f}"
        res = requests.get(url)
        mat = scipy.io.loadmat(BytesIO(res.content))
        rec = mat['eyetrackRecord']
        x, y, t = rec['x'][0,0].flatten(), rec['y'][0,0].flatten(), rec['t'][0,0].flatten()
        valid = (x != -32768) & (y != -32768)
        data.append((x[valid]/max(x[valid]), y[valid]/max(y[valid]), t[valid] - t[valid][0]))
    return data

@st.cache_resource
def download_video(video_url, save_path):
    r = requests.get(video_url)
    with open(save_path, "wb") as f:
        f.write(r.content)

def analyze_gaze(gaze_data, video_path, alpha=0.007, window=20):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w, h = int(cap.get(3)), int(cap.get(4))

    frames, convex, concave, imgs = [], [], [], []
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        pts = []
        for x, y, t in gaze_data:
            idx = (t / 1000 * fps).astype(int)
            if i in idx:
                for p in np.where(idx == i)[0]:
                    px = int(np.clip(x[p], 0, 1) * (w - 1))
                    py = int(np.clip(y[p], 0, 1) * (h - 1))
                    pts.append((px, py))
        if len(pts) >= 3:
            arr = np.array(pts)
            try: c_area = ConvexHull(arr).volume
            except: c_area = 0
            try:
                shape = alphashape.alphashape(arr, alpha)
                con_area = shape.area if shape.geom_type == 'Polygon' else 0
            except: con_area = 0
        else:
            c_area = con_area = 0
        frames.append(i)
        convex.append(c_area)
        concave.append(con_area)
        imgs.append(frame)
        i += 1
    cap.release()

    df = pd.DataFrame({'Frame': frames, 'Convex Area': convex, 'Concave Area': concave}).set_index('Frame')
    df['Convex Area (Rolling)'] = df['Convex Area'].rolling(window, min_periods=1).mean()
    df['Concave Area (Rolling)'] = df['Concave Area'].rolling(window, min_periods=1).mean()
    df['F-C score'] = 1 - (df['Convex Area (Rolling)'] - df['Concave Area (Rolling)']) / df['Convex Area (Rolling)']
    df['F-C score'] = df['F-C score'].fillna(0)
    return df, imgs

# UI
selected_video = st.selectbox("🎬 Select a video", list(video_files.keys()))
if selected_video:
    video_url = base_video_url + video_files[selected_video]
    st.video(video_url)

    if st.button("▶️ Run Analysis"):
        folder = f"{clips_folder}/{selected_video}"
        video_filename = f"{selected_video}.mp4"
        if not os.path.exists(video_filename):
            download_video(video_url, video_filename)
        with st.spinner("Analyzing..."):
            df, frames = analyze_gaze(load_gaze_data(user, repo, folder), video_filename)
            st.session_state.df = df
            st.session_state.frames = frames
            st.session_state.frame = df.index.min()

if "df" in st.session_state:
    df = st.session_state.df
    frames = st.session_state.frames
    frame = st.slider("🎞️ Select Frame", int(df.index.min()), int(df.index.max()), st.session_state.frame)

    col1, col2 = st.columns([2, 1])
    with col1:
        melted = df.reset_index().melt(id_vars="Frame", value_vars=["Convex Area (Rolling)", "Concave Area (Rolling)"], var_name="Metric", value_name="Area")
        chart = alt.Chart(melted).mark_line().encode(x="Frame:Q", y="Area:Q", color="Metric:N").properties(width=600, height=300)
        rule = alt.Chart(pd.DataFrame({'Frame': [frame]})).mark_rule(color='red').encode(x='Frame')
        st.altair_chart(chart + rule, use_container_width=True)

    with col2:
        img = frames[frame]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(rgb, caption=f"Frame {frame}", use_container_width=True)
        st.metric("F-C Score", f"{df.loc[frame, 'F-C score']:.3f}")
