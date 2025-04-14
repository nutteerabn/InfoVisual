import streamlit as st

# ตัวอย่างชื่อวิดีโอ
clip_name = st.selectbox("เลือกวิดีโอ", ["APPAL_2a"])
max_frame = 700

# Session state เก็บตำแหน่งเฟรม
if 'frame_number' not in st.session_state:
    st.session_state.frame_number = 0

# แสดงปุ่ม
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⏮ Previous"):
        st.session_state.frame_number = max(0, st.session_state.frame_number - 1)
with col2:
    if st.button("▶️ Next"):
        st.session_state.frame_number = min(max_frame, st.session_state.frame_number + 1)

# Slider (เชื่อมกับ session state)
frame_number = st.slider("เลือกตำแหน่งเฟรม", 0, max_frame, st.session_state.frame_number)
st.session_state.frame_number = frame_number  # อัปเดตค่าหลังเลื่อน

# นำ frame_number ไปใช้โหลดวิดีโอและพล็อตจุด
st.write(f"📍 เฟรมที่: {frame_number}")
