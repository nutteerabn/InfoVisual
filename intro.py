import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Understanding Viewer Focus", layout="wide")

# --- แสดงภาพแทนหัวข้อ ---
st.image("conclip/Understanding Viewer Focus Through Gaze Visualization (1).png", use_column_width=True)

# --- Introduction ---
st.markdown("""
This visualization explores how viewer attention is distributed during video watching.
We analyze the difference between **Convex Hull** and **Concave Hull** areas surrounding gaze points
to determine how focused or scattered the viewers' attention is.
""")

# --- Section: 1. Explain Convex vs Concave Hull ---
st.subheader("📐 Convex vs Concave Hull: What Do They Tell Us?")
st.markdown("""
- **Convex Hull** wraps all gaze points to capture the full boundary of visual spread.
- **Concave Hull** forms a more adaptive shape, revealing the underlying gaze distribution pattern.

> By comparing their areas, we can quantify the **focus score**, which reflects how concentrated the attention is.
""")

# --- Section: 2. Video Examples and Gaze Overlay ---
st.subheader("🎥 Example: Eye Tracking on Video")
st.markdown("Select a clip to view gaze points overlay and focus pattern.")

# 🔽 Dropdown for selecting a video (to be connected with real data)
selected_clip = st.selectbox("Choose a video clip", ["APPAL_2a", "MARCH_12a", "SIMPS_9a"])

# 👁 Placeholder: embed or play the video
st.video("path/to/sample_video.mp4")  # replace with real path later

# --- Section: 3. Score Explanation ---
st.subheader("🧠 Focus Score Explained")
st.markdown("""
The **Focus Score (F-C Score)** is calculated as the difference between convex and concave hull areas.

- A score near **1.0** → tight attention (focused).
- A score near **0.0** → widely scattered gaze (unfocused).

""")

# --- Section: 4. Visualizations ---
st.subheader("📊 Gaze Spread and Focus Score Over Time")

st.markdown("*(This section will contain convex vs concave area line charts, and score chart per frame)*")

# 🔲 Placeholder for charts (e.g. Altair or matplotlib chart can be inserted here)
st.info("📌 Chart coming soon...")

# --- Footer ---
st.markdown("---")
st.markdown("Created by your team – powered by Streamlit and Eye Tracking Analysis 💡")
