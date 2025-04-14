import streamlit as st
import streamlit.components.v1 as components

# วิดีโอจาก Google Drive (ใช้ ID -> preview)
video_ids = {
    "APPAL_2a": "1hJXZmnYPEWjCVBapWU2QRKBvOTt3yqzo",
    "Cloud_17a": "1rehRu2sIywGqHFfypJOl-F7FD34bwxK_"
}

st.title("🎥 ดูวิดีโอจาก Google Drive")

# Dropdown
selected = st.selectbox("เลือกวิดีโอ", list(video_ids.keys()))

if selected:
    file_id = video_ids[selected]
    embed_url = f"https://drive.google.com/file/d/{file_id}/preview"

    st.subheader(f"วิดีโอ: {selected}")
    components.iframe(embed_url, height=480, width=800)
