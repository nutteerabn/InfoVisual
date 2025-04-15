import streamlit as st

st.set_page_config(layout="wide")

# SECTION 1: Title (ไม่มีพื้นหลัง)
st.title("🌟 Understanding Viewer Focus Through Gaze Visualization")

# SECTION 2: Introduction + รูป + Quote + Text (พื้นหลังสีเหลืองอ่อน)
st.markdown("""
<div style="background-color: #fff9e6; padding: 25px; border-radius: 10px; margin-top: 20px;">

    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/conclip/Image.jpeg" 
         width="100%" style="border-radius: 8px; margin-bottom: 15px;">

    <blockquote style="
        font-size: 1.05em;
        text-align: center;
        font-weight: bold;
        font-style: italic;
        border-left: 6px solid #f9a825;
        background-color: #fff8dc;
        padding: 1em;
        margin: 1.5em 0;
        border-radius: 6px;">
        “Is the viewer’s attention firmly focused on key moments,<br>
        or does it float, drifting between different scenes in search of something new?”
    </blockquote>

    <p style="font-size: 1.05em;">
        The goal of this visualization is to understand how viewers engage with a video by examining where and how they focus their attention.
        By comparing the areas where viewers look (represented by convex and concave hulls), the visualization highlights whether their attention stays focused on a specific part of the video or shifts around.
    </p>

    <p style="font-size: 1.05em;">
        Ultimately, this visualization helps us uncover patterns of focus and exploration, providing insights into how viewers interact with different elements of the video.
    </p>

</div>
""", unsafe_allow_html=True)

# SECTION 3: Hull Concept
st.markdown("""
<div style="background-color: #e3f2fd; padding: 25px; border-radius: 10px; margin-top: 30px;">

    <h3>📐 How Do We Measure Focus?</h3>
    <p style="font-size: 1.05em;">
        We use geometric shapes to visualize how tightly the viewer’s gaze is grouped:
    </p>

    <ul style="font-size: 1.05em;">
        <li><strong>Convex Hull</strong>: Encloses all gaze points loosely.</li>
        <li><strong>Concave Hull</strong>: Follows the actual shape of gaze, revealing true focus.</li>
    </ul>

    <p style="font-size: 1.05em;">
        👉 The <strong>difference in area</strong> between the two tells us how spread out or concentrated the gaze is.
    </p>

    <div style="display: flex; gap: 2%; margin-top: 20px;">
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_image.jpg" width="48%">
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_SIMPS_9a.gif" width="48%">
    </div>

</div>
""", unsafe_allow_html=True)

# SECTION 4: F-C Score
st.markdown("""
<div style="background-color: #fff3e0; padding: 25px; border-radius: 10px; margin-top: 30px;">

    <h3>📊 Focus-Concentration (F-C) Score</h3>

    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/formula_image.jpeg" 
         width="100%" style="border-radius: 8px; margin: 10px 0 20px 0;">

    <p style="font-size: 1.05em;">
        The <strong>F-C Score</strong> helps quantify gaze behavior:
    </p>

    <ul style="font-size: 1.05em;">
        <li><strong>Close to 1</strong> → tight gaze cluster → <span style="color:#2e7d32;"><strong>high concentration</strong></span></li>
        <li><strong>Much lower than 1</strong> → scattered gaze → <span style="color:#c62828;"><strong>low concentration</strong></span></li>
    </ul>

    <p style="font-size: 1.05em;">
        This metric reveals whether attention is <strong>locked in</strong> or <strong>wandering</strong>.
    </p>

</div>
""", unsafe_allow_html=True)

# SECTION 5: Visual Examples
st.markdown("""
<div style="background-color: #f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">

    <h3>🎥 Visual Examples of Focus</h3>

    <div style="display: flex; gap: 2%;">
        <div style="width: 49%;">
            <h4>High F-C Score</h4>
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_high_F-C_score.gif" width="100%">
            <p style="text-align:center; font-size: 0.95em;">Gaze remains tightly grouped in one region.</p>
        </div>

        <div style="width: 49%;">
            <h4>Low F-C Score</h4>
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_low_F-C_score.gif" width="100%">
            <p style="text-align:center; font-size: 0.95em;">Gaze jumps around, showing exploration or distraction.</p>
        </div>
    </div>

    <p style="margin-top: 20px; font-size: 1.05em;">
        You’ll see this visualized dynamically in the graph and overlays as you explore different segments of the video.
    </p>

</div>
""", unsafe_allow_html=True)
