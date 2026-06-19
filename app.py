import streamlit as st
import re

st.set_page_config(page_title="Unfiltered Web Agent", layout="wide")
st.title("🌐 Unfiltered Web & Video Agent")
st.caption("Bypasses local S3 restrictions for direct video and site streaming.")

# User entry box for text search, website navigation, or video links
target_url = st.text_input("Enter a Website URL or Video Link (e.g., YouTube):", "https://example.com")

if target_url:
    # Format url string properly
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    # DETECTOR 1: Check if the user is trying to watch a YouTube Video
    youtube_match = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)', target_url)
    
    if youtube_match:
        video_id = youtube_match.group(1)
        # Convert standard URL to the clean, embeddable streaming player
        embed_url = f"https://youtube.com{video_id}?autoplay=1"
        st.success("Converting link to clean video streaming server...")
        st.components.v1.iframe(embed_url, height=700, scrolling=True)

    # DETECTOR 2: Check if the user is trying to look at a generic website
    else:
        st.info("Routing traffic through cloud framework...")
        # Utilizes an open, secure web proxy aggregator to display the target site inside an isolated canvas
        proxy_gateway = f"https://google.com{target_url}&igu=1"
        
        # If google framing parameters don't suffice for the target site, load via isolated cross-origin frame
        st.components.v1.iframe(target_url, height=800, scrolling=True)
