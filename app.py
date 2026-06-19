import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# Import curl_cffi to masquerade perfectly as a real desktop browser
from curl_cffi import requests

st.set_page_config(page_title="Unfiltered Web Agent", layout="wide")
st.title("🌐 Unfiltered Web Agent")
st.caption("Bypasses local S3 restrictions by proxying requests.")

target_url = st.text_input("Enter the URL you wish to visit:", "https://example.com")

if target_url:
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        with st.spinner(f"Agent fetching {target_url}..."):
            # Use curl_cffi session configured to impersonate a real Chrome browser on Windows
            # verify=False is automatically included here to continue bypassing the S3 certificate filter
            response = requests.get(
                target_url, 
                impersonate="chrome", 
                timeout=15, 
                verify=False
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                base_url = response.url

                for tag in soup.find_all(["img", "link", "script"]):
                    attr = "src" if tag.name in ["img", "script"] else "href"
                    if tag.has_attr(attr):
                        tag[attr] = urljoin(base_url, tag[attr])

                st.success(f"Successfully loaded: {target_url}")
                st.components.v1.html(str(soup), height=800, scrolling=True)
            else:
                st.error(f"Failed to load website. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"The agent could not access the site. Error: {e}")
