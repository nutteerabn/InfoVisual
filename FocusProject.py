import streamlit as st
import os
import cv2
import altair as alt
import pandas as pd
from utils import load_gaze_data, download_video, analyze_gaze

# 🧱 Config ต้องอยู่บรรทัดแรก
st.set_page_config(layout="wide", page_title="Gaze Hull Visualizer")

# 💡 CSS สำหรับ animation
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

# -------------------- 🎯 TITLE ---------------------
st.image("conclip/Image.jpeg", use_container_width=True)

# -------------------- 📌 SECTION 1 ---------------------
st.markdown("""
<div class="popup-section section-1" style="background-color: #DCEEFF; padding: 25px; border-radius: 10px; margin-top: 30px;">
<blockquote style="
    font-size: 1.1em;
    text-align: center;
    font-weight: bold;
    font-style: italic;
    border-left: 6px solid #95A5A6;
    background-color: #ECF0F1;
    padding: 1em;
    margin: 1.5em 0;
    border-radius: 6px;">
    “Is the viewer’s attention firmly focused on key moments,<br>
    or does it float, drifting between different scenes in search of something new?”
</blockquote>
<p style="font-size: 1.05em;">
    This visualization explores how viewers engage with a video by examining where and how they focus their attention.
</p>
</div>
""", unsafe_allow_html=True)

# -------------------- 📐 SECTION 2 ---------------------
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
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_image.jpg"
             style="width: 100%; border-radius: 8px;" alt="Diagram of Convex and Concave Hulls">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; margin-top: 8px;">
            📊 Diagram: Convex vs Concave Hulls
        </p>
    </div>
    <div style="width: 48%;">
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_SIMPS_9a.gif"
             style="width: 100%; border-radius: 8px;" alt="Gaze Boundaries Example">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; margin-top: 8px;">
            🎥 Real Example: Gaze Boundaries Over Time
        </p>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# -------------------- 📊 SECTION 3 ---------------------
st.markdown("""
<div class="popup-section section-3" style="background-color:#f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">
<h3>📊 Focus-Concentration (F-C) Score</h3>
<img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/formula_image.jpeg"
     style="width: 100%; border-radius: 8px;" alt="Formula Example">
<p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic; margin-top: 8px;">
    🧮 Area calculation using a rolling average across the last 20 frames
</p>
<p style="font-size: 1.05em;">
    The <b>F-C Score</b> helps quantify gaze behavior:
</p>
<ul style="font-size: 1.05em;">
    <li><b>Close to 1</b> → tight gaze cluster → <span style="color:#2e7d32;"><b>high concentration</b></span>.</li>
    <li><b>Much lower than 1</b> → scattered gaze → <span style="color:#d32f2f;"><b>low concentration / exploration</b></span>.</li>
</ul>
<p style="font-size: 1.05em;">
    This metric reveals whether attention is <b>locked in</b> or <b>wandering</b>.
</p>
</div>
""", unsafe_allow_html=True)

# -------------------- 🎥 SECTION 4 ---------------------
st.markdown("""
<div class="popup-section section-4" style="background-color: #f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">
<h3>🎥 Visual Examples of Focus</h3>
<div style="display: flex; gap: 20px;">
    <div style="width: 50%;">
        <h4>High F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_high_F-C_score.gif"
             style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic;">
            Gaze remains tightly grouped in one region.
        </p>
    </div>
    <div style="width: 50%;">
        <h4>Low F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_low_F-C_score.gif"
             style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center; color: #6c757d; font-style: italic;">
            Gaze jumps around, showing exploration or distraction.
        </p>
    </div>
</div>
<p style="font-size: 1.05em; margin-top: 1.5em;">
    You’ll see this visualized dynamically in the graph and overlays as you explore different segments of the video.
</p>
</div>
""", unsafe_allow_html=True)

# -------------------- 🔻 Section Divider ---------------------
st.markdown("""
<hr style="margin-top: 50px; margin-bottom: 50px; border: none; border-top: 3px dashed #ccc;">
<h2 style="text-align: center; font-size: 1.8em; color: #2f3542; font-weight: bold;">🔍 Interactive Focus Dashboard</h2>
<p style="text-align: center; font-size: 1.05em; color: #57606f;">
    Select a video and explore how gaze patterns change frame by frame.
</p>
""", unsafe_allow_html=True)

# -------------------- 📈 INTERACTIVE ANALYSIS ---------------------
@st.cache_data
def get_gaze_and_analysis(user, repo, folder, video_url, video_filename):
    gaze = load_gaze_data(user, repo, folder)
    if not os.path.exists(video_filename):
        download_video(video_url, video_filename)
    return analyze_gaze(gaze, video_filename)

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

selected_video = st.selectbox("🎬 Select a video", list(video_files.keys()))

if selected_video:
    st.video(base_video_url + video_files[selected_video])
    folder = f"{clips_folder}/{selected_video}"
    video_filename = f"{selected_video}.mp4"

    with st.spinner("Running analysis..."):
        df, frames = get_gaze_and_analysis(
            user, repo, folder, base_video_url + video_files[selected_video], video_filename
        )
        st.session_state.df = df
        st.session_state.frames = frames
        st.session_state.frame_min = int(df.index.min())
        st.session_state.frame_max = int(df.index.max())
        st.session_state.chart_data = df.reset_index().melt(
            id_vars="Frame", 
            value_vars=["Convex Area (Rolling)", "Concave Area (Rolling)"], 
            var_name="Metric", 
            value_name="Area"
        )

if "df" in st.session_state:
    frame = st.slider(
        "🎞️ Select Frame", 
        st.session_state.frame_min, 
        st.session_state.frame_max, 
        st.session_state.frame_min
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        base_chart = alt.Chart(st.session_state.chart_data).mark_line().encode(
            x="Frame:Q", y="Area:Q", color="Metric:N"
        ).properties(width=600, height=300)
        rule = alt.Chart(pd.DataFrame({'Frame': [frame]})).mark_rule(color='red').encode(x='Frame:Q')
        st.altair_chart(base_chart + rule, use_container_width=True)

    with col2:
        rgb = cv2.cvtColor(st.session_state.frames[frame], cv2.COLOR_BGR2RGB)
        st.image(rgb, caption=f"Frame {frame}", use_container_width=True)
        st.metric("F-C Score", f"{st.session_state.df.loc[frame, 'F-C score']:.3f}")
