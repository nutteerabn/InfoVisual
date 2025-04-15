import streamlit as st

st.set_page_config(layout="wide")

# ===== CSS STYLE =====
st.markdown("""
    <style>
    .custom-section {
        background-color: #f5f5f5;
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .custom-section h1, .custom-section h2, .custom-section h3 {
        margin-top: 0;
    }
    .custom-section img {
        border-radius: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    .quote {
        font-size: 1.1em;
        text-align: center;
        font-weight: bold;
        font-style: italic;
        border-left: 6px solid #f9a825;
        background-color: #fff8dc;
        padding: 1em;
        margin: 1.5em 0;
        border-radius: 6px;
    }
    ul {
        margin: 0;
        padding-left: 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

# ===== SECTION 1: Hook =====
st.markdown("""
<div class="custom-section">
    <h1>🌟 Understanding Viewer Focus Through Gaze Visualization</h1>

    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/conclip/Image.jpeg" alt="Header Image">

    <div class="quote">
        “Is the viewer’s attention firmly focused on key moments,<br>
        or does it float, drifting between different scenes in search of something new?”
    </div>

    <p style="font-size: 1.05em;">
        The goal of this visualization is to understand how viewers engage with a video by examining where and how they focus their attention.
        By comparing the areas where viewers look (represented by convex and concave hulls), the visualization highlights whether their attention stays focused on a specific part of the video or shifts around.
    </p>

    <p style="font-size: 1.05em;">
        Ultimately, this visualization helps us uncover patterns of focus and exploration, providing insights into how viewers interact with different elements of the video.
    </p>
</div>
""", unsafe_allow_html=True)

# ===== SECTION 2: Hull Concept =====
st.markdown("""
<div class="custom-section">
    <h2>📊 How Do We Measure Focus?</h2>

    <p>We use geometric shapes to visualize how tightly the viewer’s gaze is grouped:</p>

    <ul>
        <li><strong>Convex Hull</strong>: Encloses all gaze points loosely.</li>
        <li><strong>Concave Hull</strong>: Follows the actual shape of gaze, revealing true focus.</li>
    </ul>

    <p>🔀 The <strong>difference in area</strong> between the two tells us how spread out or concentrated the gaze is.</p>

    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 280px;">
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_image.jpg" alt="Diagram">
            <p style="text-align: center;">Diagram: Convex vs Concave Hulls</p>
        </div>
        <div style="flex: 1; min-width: 280px;">
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/convex_concave_SIMPS_9a.gif" alt="Real Example">
            <p style="text-align: center;">Real Example: Gaze Boundaries Over Time</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== SECTION 3: F-C Score =====
st.markdown("""
<div class="custom-section">
    <h2>📊 Focus-Concentration (F-C) Score</h2>

    <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/formula_image.jpeg" alt="Formula" style="width: 100%;">

    <p style="font-size: 1.05em;">
        The <strong>F-C Score</strong> helps quantify gaze behavior:
    </p>

    <ul>
        <li><strong>Close to 1</strong> → tight gaze cluster → <span style="color:#2e7d32; font-weight:bold;">high concentration</span></li>
        <li><strong>Much lower than 1</strong> → scattered gaze → <span style="color:#c62828; font-weight:bold;">low concentration</span></li>
    </ul>

    <p>This metric reveals whether attention is <strong>locked in</strong> or <strong>wandering</strong>.</p>
</div>
""", unsafe_allow_html=True)

# ===== SECTION 4: Visual Examples =====
st.markdown("""
<div class="custom-section">
    <h2>🎥 Visual Examples of Focus</h2>

    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 280px;">
            <h4>High F-C Score</h4>
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_high_F-C_score.gif">
            <p style="text-align: center;">Gaze remains tightly grouped in one region.</p>
        </div>
        <div style="flex: 1; min-width: 280px;">
            <h4>Low F-C Score</h4>
            <img src="https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/gif_sample/FOODI_2a_low_F-C_score.gif">
            <p style="text-align: center;">Gaze jumps around, showing exploration or distraction.</p>
        </div>
    </div>

    <p>You’ll see this visualized dynamically in the graph and overlays as you explore different segments of the video.</p>
</div>
""", unsafe_allow_html=True)
