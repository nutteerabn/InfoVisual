import streamlit as st
import streamlit.components.v1 as components

video_url = "https://www.example.com/video.mp4"  # ต้องเป็นลิงก์ .mp4 ตรงๆ

components.html(f"""
    <video id="myVideo" width="800" controls>
      <source src="{video_url}" type="video/mp4">
      Your browser does not support the video tag.
    </video>

    <br>
    <input type="range" id="slider" min="0" max="100" value="0" style="width:800px">

    <script>
    const video = document.getElementById("myVideo");
    const slider = document.getElementById("slider");

    // Sync slider <-> video
    video.ontimeupdate = function() {{
        slider.value = (video.currentTime / video.duration) * 100;
    }};
    slider.oninput = function() {{
        video.currentTime = (slider.value / 100) * video.duration;
    }};
    </script>
""", height=500)
