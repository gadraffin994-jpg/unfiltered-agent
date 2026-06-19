import streamlit as st
import os
import subprocess
import asyncio

# --- CRITICAL CLOUD FIX: Force Playwright to download binaries on Streamlit Cloud ---
@st.cache_resource
def ensure_playwright_browsers():
    try:
        # Check if the playwright cache directory exists and has contents
        playwright_path = os.path.expanduser("~/.cache/ms-playwright")
        if not os.path.exists(playwright_path) or len(os.path.listdir(playwright_path)) == 0:
            with st.spinner("First-time setup: Installing unblocked cloud browser binaries (this takes ~30s)..."):
                # Run the installation command directly into the Linux environment hosting your app
                subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Browser installation pre-flight failed: {e}")

# Trigger the browser check/install before the rest of the application loads
ensure_playwright_browsers()

# --- Rest of your interactive async application ---
from playwright.async_api import async_playwright

st.set_page_config(page_title="Unfiltered Cloud Agent", layout="wide")
st.title("🌐 Fully Interactive Web & Video Agent")
st.caption("Running securely in the cloud to completely bypass local network restrictions.")

target_url = st.text_input("Enter a Website URL or Video Link (e.g., YouTube):", "https://youtube.com")

async def fetch_page_cloud(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle", timeout=30000)
        content = await page.content()
        await browser.close()
        return content

if target_url:
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        with st.spinner("Cloud agent spin-up: executing JavaScript and rendering interactive streams..."):
            rendered_html = asyncio.run(fetch_page_cloud(target_url))
            st.success(f"Fully rendered via Cloud Pipeline: {target_url}")
            st.components.v1.html(rendered_html, height=900, scrolling=True)

    except Exception as e:
        st.error(f"The cloud agent hit an execution bottleneck. Details: {e}")
