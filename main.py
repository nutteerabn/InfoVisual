import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎥 ดูวิดีโอ + แถบเลื่อนเวลา")

# === วิดีโอ URL ตรง (.mp4)
video_urls = {
    "APPAL_2a": "https://drive.google.com/uc?export=download&id=1hJXZmnYPEWjCVBapWU2QRKBvOTt3yqzo",
    "Cloud_17a": "https://drive.google.com/uc?export=download&id=1rehRu2sIywGqHFfypJOl-F7FD34bwxK_"
}

# === Dropdown
selected = st.selectbox("เลือกวิดีโอ", list(video_urls.keys()))

# === แสดงวิดีโอด้วย HTML + JS
if selected:
    video_url = video_urls[selected]

    components.html(f"""
    <video id="myVideo" width="800" height="450" controls>
      <source src="{video_url}" type="video/mp4">
      Your browser does not support the video tag.
    </video>

    <br>
    <input type="range" id="slider" min="0" max="100" value="0" style="width:800px">

    <script>
    const video = document.getElementById("myVideo");
    const slider = document.getElementById("slider");

    video.ontimeupdate = function() {{
        const value = (video.currentTime / video.duration) * 100;
        slider.value = value;
    }};

    slider.oninput = function() {{
        const newTime = (slider.value / 100) * video.duration;
        video.currentTime = newTime;
    }};
    </script>
    """, height=520)
