import streamlit as st

st.set_page_config(layout="wide")

# -------------------- 🎯 TITLE ---------------------
st.title("🌟 Understanding Viewer Focus Through Gaze Visualization")

# -------------------- 🎯 SECTION 1 ---------------------
st.markdown("""
<div style="background-color: #fff8dc; padding: 25px; border-radius: 10px; margin-top: 20px;">

    <h2>📌 What Captures Attention?</h2>

    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/conclip/Image.jpeg"
         width="100%" style="border-radius: 8px; margin-bottom: 15px;">

    <blockquote style="
        font-size: 1.05em;
        text-align: center;
        font-weight: bold;
        font-style: italic;
        border-left: 6px solid #f9a825;
        background-color: #fffde7;
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

# -------------------- 📐 SECTION 2 ---------------------
st.markdown("""
<div style="background-color: #e0f7fa; padding: 25px; border-radius: 10px; margin-top: 30px;">

<h3>📐 How Do We Measure Focus?</h3>

<p style="font-size: 1.05em;">We use geometric shapes to visualize how tightly the viewer’s gaze is grouped:</p>

<ul style="font-size: 1.05em;">
    <li><b>Convex Hull</b>: Encloses all gaze points loosely.</li>
    <li><b>Concave Hull</b>: Follows the actual shape of gaze, revealing true focus.</li>
</ul>

<p style="font-size: 1.05em;">👉 The <b>difference in area</b> between the two tells us how spread out or concentrated the gaze is.</p>

<div style="display: flex; gap: 20px;">
    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_image.jpg"
         style="width: 48%; border-radius: 8px;" alt="Diagram of Convex and Concave Hulls">
    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_SIMPS_9a.gif"
         style="width: 48%; border-radius: 8px;" alt="Gaze Boundaries Example">
</div>

</div>
""", unsafe_allow_html=True)

# -------------------- 📊 SECTION 3 ---------------------
st.markdown("""
<div style="background-color: #fff3e0; padding: 25px; border-radius: 10px; margin-top: 30px;">

<h3>📊 Focus-Concentration (F-C) Score</h3>

<img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/formula_image.jpeg"
     style="width: 100%; border-radius: 8px;" alt="Formula Example">

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
<div style="background-color: #f3e5f5; padding: 25px; border-radius: 10px; margin-top: 30px;">

<h3>🎥 Visual Examples of Focus</h3>

<div style="display: flex; gap: 20px;">
    <div style="width: 50%;">
        <h4>High F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_high_F-C_score.gif"
             style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center;">Gaze remains tightly grouped in one region.</p>
    </div>
    <div style="width: 50%;">
        <h4>Low F-C Score</h4>
        <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_low_F-C_score.gif"
             style="width: 100%; border-radius: 8px;">
        <p style="font-size: 0.95em; text-align: center;">Gaze jumps around, showing exploration or distraction.</p>
    </div>
</div>

<p style="font-size: 1.05em;">
    You’ll see this visualized dynamically in the graph and overlays as you explore different segments of the video.
</p>

</div>
""", unsafe_allow_html=True)
