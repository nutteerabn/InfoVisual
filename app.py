import streamlit as st
import utils

st.set_page_config(page_title="InfoVisual Dashboard", layout="wide")

st.title("🎬 Eye Gaze Visual Dashboard")
st.markdown("อัปโหลดวิดีโอและดูพฤติกรรมการมอง (Convex vs Concave Hull Area)")

# ตัวเลือกไฟล์จาก Google Drive
video_choices = {
    "APPAL_2a": "your_file_id_here",
    "NANN_3a": "your_file_id_here"
}

video_label = st.selectbox("เลือกคลิปวิดีโอ", list(video_choices.keys()))

video_url = f"https://drive.google.com/uc?id={video_choices[video_label]}"
st.video(video_url)

# กราฟ
df = utils.get_convex_concave_data(video_label)  # ตัวอย่างฟังก์ชันจาก utils
st.line_chart(df[['Convex Area (Rolling Avg)', 'Concave Area (Rolling Avg)']])
