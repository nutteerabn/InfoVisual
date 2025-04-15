import streamlit as st

# แสดงภาพหัวข้อ
st.image("conclip/Image.jpeg", use_column_width=True)

# 🧭 แท็บเนื้อหาแต่ละพาร์ท
tab1, tab2, tab3, tab4 = st.tabs(["1. Introduction", "2. Concept", "3. Visualization", "4. Interpretation"])

with tab1:
    st.subheader("1. Introduction")
    st.write("Introduce the goal of this visualization...")

with tab2:
    st.subheader("2. Convex & Concave Hull")
    st.write("""
    Convex Hull wraps all gaze points to show the outer boundary of visual spread.  
    Concave Hull follows the true shape of gaze clusters more tightly.
    Comparing their areas helps us quantify how focused or dispersed the gaze is.
    """)

with tab3:
    st.subheader("3. Visualization Example")
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
