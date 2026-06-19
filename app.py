import streamlit as st
import os
import sys
import asyncio

# --- PRODUCTION CLOUD FIX: Native Playwright Installer Bypass ---
@st.cache_resource
def cloud_preflight_install():
    # Streamlit Cloud isolates its cache here. If it's missing, force the install.
    cache_dir = os.path.expanduser("~/.cache/ms-playwright")
    if not os.path.exists(cache_dir) or not os.listdir(cache_dir):
        with st.spinner("Configuring unblocked cloud browser pipeline... This takes about 30 seconds."):
            try:
                # Using sys.executable guarantees it uses the exact Python path Streamlit is running on
                os.system(f"{sys.executable} -m playwright install chromium")
            except Exception as e:
                st.error(f"Pre-flight setup warning: {e}")

# Run the installer check immediately on launch
cloud_preflight_install()

# --- Core Web Agent ---
from playwright.async_api import async_playwright

st.set_page_config(page_title="Unfiltered Cloud Agent", layout="wide")
st.title("🌐 Fully Interactive Web & Video Agent")
st.caption("Running securely via isolated cloud architecture to bypass network blocks.")

target_url = st.text_input("Enter a Website URL or Video Link (e.g., YouTube):", "https://youtube.com")

async def fetch_page_cloud(url):
    async with async_playwright() as p:
        # Launch using strict headless sandbox flags required by Streamlit's Linux container
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
        )
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        
        page = await context.new_page()
        # Navigate and wait until the single page app settles down and loads content streams
        await page.goto(url, wait_until="networkidle", timeout=45000)
        
        content = await page.content()
        await browser.close()
        return content

if target_url:
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        with st.spinner("Cloud agent routing traffic and bypassing filters..."):
            rendered_html = asyncio.run(fetch_page_cloud(target_url))
            st.success(f"Fully rendered via Cloud Pipeline: {target_url}")
            st.components.v1.html(rendered_html, height=900, scrolling=True)

    except Exception as e:
        st.error(f"The cloud agent encountered an execution hurdle. Details: {e}")
