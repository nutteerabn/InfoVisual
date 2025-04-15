import streamlit as st
st.markdown("""
    <style>
        * {
            font-family: 'Helvetica Neue', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# หัวข้อรูปภาพด้านบน
st.image("conclip/Image.jpeg", use_container_width=True)

# สร้างแท็บ
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Visualization Goal", 
    "2. Convex & Concave Hull", 
    "3. F-C Score", 
    "4. Example: High vs Low F-C Score"
])

# ⬅️ แท็บที่ 1 : Visualization Goal
with tab1:
    st.subheader("🎯 Goal of This Visualization")

    st.markdown("""
<blockquote style="font-size: 1em; text-align: center; font-weight: bold; font-style: italic; border-left: 4px solid #999; padding-left: 1em; margin: 1.5em 0;">
    “Is the viewer’s attention firmly focused on key moments,<br>
    or does it float, drifting between different scenes in search of something new?”
</blockquote>
""", unsafe_allow_html=True)
    
    st.write("""
    The goal of this visualization is to understand how viewers engage with a video by examining where and how they focus their attention. By comparing the areas where viewers look (represented by convex and concave hulls), the visualization highlights whether their attention stays focused on a specific part of the video or shifts around.

    Ultimately, this visualization helps us uncover patterns of focus and exploration, providing insights into how viewers interact with different elements of the video.
    """)

with tab2:
    st.subheader("📐 Convex & Concave Hull Concept")

    st.write("To analyze visual attention, we enclose gaze points with geometric boundaries:")

    st.markdown("""
    <div style='padding: 0.5em; background-color: #e6f0ff; border-left: 4px solid #1e88e5; margin: 1em 0'>
        <ul style='margin: 0; padding-left: 1.2em;'>
            <li><strong>Convex Hull</strong> wraps around all gaze points to show the overall extent of where viewers looked.</li>
            <li><strong>Concave Hull</strong> creates a tighter boundary that closely follows the actual shape of the gaze pattern, adapting to gaps and contours in the data.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("The difference in area between them reveals how dispersed or concentrated the viewers’ gaze is.")

with tab3:
    st.subheader("📊 Focus Concentration (F-C) Score")

    st.write("""
    The Focus Concentration Score (FCS) quantifies how focused or scattered a viewer's attention is during the video.""")

    st.markdown("""
    <div style='padding: 0.7em; background-color: #f0f8ff; border-left: 5px solid #1976d2; margin: 1em 0; font-size: 1.05em'>
        <ul style='margin: 0; padding-left: 1.2em;'>
            <li><strong>Score close to 1.0</strong> → Gaze is tightly grouped → <span style="color:#2e7d32;"><strong>High concentration</strong></span></li>
            <li><strong>Score much lower than 1.0</strong> → Gaze is more spread out → <span style="color:#d32f2f;"><strong>Lower concentration / Exploration</strong></span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("It helps to measure whether attention is locked onto a specific spot or wandering across the frame.")


with tab4:
    st.subheader("🎬 Example: High vs Low F-C Score")

    st.markdown("""
    <div style='padding: 0.7em; background-color: #f9f9f9; border-left: 5px solid #90caf9; margin: 1em 0; font-size: 1.05em'>
        <ul style='margin: 0; padding-left: 1.2em;'>
            <li><strong>High F-C Score</strong>: The viewer’s gaze remains focused in one tight area, suggesting <span style='color:#2e7d32'><strong>strong interest or attention</strong></span>.</li>
            <li><strong>Low F-C Score</strong>: The gaze is scattered, moving across many regions of the screen, indicating <span style='color:#c62828'><strong>exploration or distraction</strong></span>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("You can observe this difference visually in the graph and video overlays as you explore different frames.")

# 🔻 พาร์ทที่ 5 และ 6 อยู่ด้านล่างแบบไม่อยู่ในแท็บ
st.markdown("---")
st.subheader("5. Graph: Focus-Score over Time")
# 📈 Insert Altair/Plotly graph here

st.subheader("6. Summary Insight")
st.write("Summarize insight from graph or video patterns.")
