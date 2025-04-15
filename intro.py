import streamlit as st

# หัวข้อรูปภาพด้านบน
st.image("conclip/Image.jpeg", use_column_width=True)

# สร้างแท็บ
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Visualization Goal", 
    "2. Convex & Concave Hull", 
    "3. F-C Score", 
    "4. Interpretation"
])

# ⬅️ แท็บที่ 1 : Visualization Goal
with tab1:
    st.subheader("🎯 Goal of This Visualization")

    st.markdown("""
    > *“Is the viewer’s attention firmly focused on key moments,  
    > or does it float, drifting between different scenes in search of something new?”*
    """, unsafe_allow_html=True)

    st.write("""
    The goal of this visualization is to understand how viewers engage with a video by examining where and how they focus their attention. By comparing the areas where viewers look (represented by convex and concave hulls), the visualization highlights whether their attention stays focused on a specific part of the video or shifts around.

    Ultimately, this visualization helps us uncover patterns of focus and exploration, providing insights into how viewers interact with different elements of the video.
    """)

with tab2:
    st.subheader("🌀 Convex & Concave Hull Concept")

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
    st.subheader("📝 Focus Concentration (F-c) Score")
    # 👁️ Insert dynamic visualization (e.g. video + hull overlays)

with tab4:
    st.subheader("4. Interpretation of the Score")
    st.write("""
    - Score near **1.0** → High concentration
    - Score closer to **0** → Scattered gaze / low attention
    """)

# 🔻 พาร์ทที่ 5 และ 6 อยู่ด้านล่างแบบไม่อยู่ในแท็บ
st.markdown("---")
st.subheader("5. Graph: Focus-Score over Time")
# 📈 Insert Altair/Plotly graph here

st.subheader("6. Summary Insight")
st.write("Summarize insight from graph or video patterns.")
