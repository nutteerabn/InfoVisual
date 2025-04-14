import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="centered")
st.title("🎬 Gaze Video Viewer Dashboard (Interactive Slider)")

# ✅ GitHub video URLs (must be raw and streamable)
video_links = {
    "APPAL_2a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/APPAL_2a_c.mp4",
    "NANN_3a": "https://raw.githubusercontent.com/nutteerabn/InfoVisual/main/Clips%20(small%20size)/NANN_3a_c.mp4"
}

# ✅ Dropdown
selected = st.selectbox("เลือกวิดีโอ", list(video_links.keys()))
video_url = video_links[selected]

# ✅ ฝัง HTML + JS
html_code = f"""
<!DOCTYPE html>
<html>
<body>

<video id="myVideo" width="700" controls>
  <source src="{video_url}" type="video/mp4">
  Your browser does not support HTML video.
</video>

<br>
<input type="range" id="slider" min="0" value="0" step="0.1" style="width: 700px;" />

<script>
  const video = document.getElementById("myVideo");
  const slider = document.getElementById("slider");

  video.addEventListener('loadedmetadata', function() {{
    slider.max = video.duration;
  }});

  video.ontimeupdate = function() {{
    slider.value = video.currentTime;
  }};

  slider.oninput = function() {{
    video.currentTime = slider.value;
  }};
</script>

</body>
</html>
"""

# ✅ แสดงใน Streamlit
components.html(html_code, height=500)
