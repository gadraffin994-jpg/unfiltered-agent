import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from curl_cffi import requests

st.set_page_config(page_title="Unfiltered Web Agent", layout="wide")
st.title("🌐 Unfiltered Web & Video Agent")
st.caption("Bypasses local S3 restrictions and frame blocks by proxying requests.")

target_url = st.text_input("Enter a Website URL or Video Link (e.g., YouTube):", "https://youtube.com")

if target_url:
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        with st.spinner(f"Agent routing traffic and bypassing filters for {target_url}..."):
            # Fetch the webpage using the Chrome impersonator to clear the network filter
            response = requests.get(
                target_url, 
                impersonate="chrome", 
                timeout=15, 
                verify=False
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                base_url = response.url

                # Rewrite asset links (images, styles, scripts) so they load via absolute URL
                for tag in soup.find_all(["img", "link", "script"]):
                    attr = "src" if tag.name in ["img", "script"] else "href"
                    if tag.has_attr(attr):
                        tag[attr] = urljoin(base_url, tag[attr])

                # Fix for YouTube specific embedding limitations inside iframes
                # This injects a base target tag to prevent the iframe from breaking out
                if "youtube.com" in target_url:
                    base_tag = soup.new_tag("base", target="_blank")
                    if soup.head:
                        soup.head.insert(0, base_tag)

                st.success(f"Successfully bypassed blocks for: {target_url}")
                
                # Render the HTML block directly. Since we are serving the modified raw HTML
                # string, the browser won't enforce the destination server's initial X-Frame headers.
                st.components.v1.html(str(soup), height=800, scrolling=True)
            else:
                st.error(f"Failed to load website. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"The agent could not access the site. Error: {e}")
