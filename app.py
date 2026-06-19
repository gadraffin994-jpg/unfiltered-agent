import streamlit as st
import asyncio
from playwright.async_api import async_playwright

st.set_page_config(page_title="Unfiltered Cloud Agent", layout="wide")
st.title("🌐 Fully Interactive Web & Video Agent")
st.caption("Running securely in the cloud to completely bypass local network restrictions.")

target_url = st.text_input("Enter a Website URL or Video Link (e.g., YouTube):", "https://youtube.com")

async def fetch_page_cloud(url):
    async with async_playwright() as p:
        # Launching with specific arguments required for headless execution in Linux cloud containers
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True  # Completely strips any remaining SSL layer blocks
        )
        
        page = await context.new_page()
        
        # Navigate and wait for the SPA/JavaScript to fully fetch the dynamic video elements
        await page.goto(url, wait_until="networkidle", timeout=30000)
        
        # Capture the living DOM content completely rendered by the cloud server
        content = await page.content()
        await browser.close()
        return content

if target_url:
    if not target_url.startswith(("http://", "https://")):
        target_url = "https://" + target_url

    try:
        with st.spinner("Cloud agent spin-up: executing JavaScript and rendering interactive streams..."):
            # Run the async browser controller cleanly inside Streamlit's environment
            rendered_html = asyncio.run(fetch_page_cloud(target_url))
            
            st.success(f"Fully rendered via Cloud Pipeline: {target_url}")
            
            # Pipe the fully built, unblocked interactive window back down to your viewport
            st.components.v1.html(rendered_html, height=900, scrolling=True)

    except Exception as e:
        st.error(f"The cloud agent hit an execution bottleneck. Details: {e}")
