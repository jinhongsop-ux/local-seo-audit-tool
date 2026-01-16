import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import time
import validators

# Import custom modules
from modules import browser, meta_analyzer, content_analyzer, link_analyzer, technical_analyzer, scoring

st.set_page_config(
    page_title="SEO Audit Tool",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for UI enhancements
st.markdown("""
<style>
    .score-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
    .pass { color: green; font-weight: bold; }
    .fail { color: red; font-weight: bold; }
    .warning { color: orange; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Advanced Local SEO Audit Tool")
st.markdown("Analyze on-page SEO factors with JavaScript rendering support.")

# Input Section
url = st.text_input("Enter URL to Audit:", placeholder="https://example.com")
analyze_btn = st.button("Start SEO Audit", type="primary")

if analyze_btn and url:
    if not validators.url(url):
        st.error("Please enter a valid URL (including http:// or https://).")
    else:
        with st.spinner("Initializing Browser & Rendering Page... (This checks for JS content)"):
            html_content, status_code, response_time, final_url = browser.fetch_page_content(url)
            
        if status_code == 0:
            st.error("Failed to connect to the website. Please check the URL and internet connection.")
        elif status_code >= 400:
            st.error(f"Error: Received HTTP {status_code} from the server.")
        else:
            st.success(f"Successfully crawled {final_url} (Status: {status_code}, Time: {response_time}ms)")
            
            # Parsing
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Run Analysis Modules
            with st.spinner("Analyzing Meta Data & Content..."):
                meta_res = meta_analyzer.analyze_meta(soup, final_url)
                content_res = content_analyzer.analyze_content(soup)
                tech_res = technical_analyzer.analyze_technical(final_url, response_time, soup)
            
            with st.spinner("Checking Link Health (Parallel)..."):
                link_res = link_analyzer.analyze_links(soup, final_url)
            
            # Calculate Score
            score_data = scoring.calculate_score(meta_res, content_res, link_res, tech_res)
            
            # --- Results Dashboard ---
            st.divider()
            
            # Score Overview
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total SEO Score", f"{score_data['total']}/100")
            with col2:
                st.metric("Meta Data", f"{score_data['breakdown']['meta']}/25")
            with col3:
                st.metric("Content", f"{score_data['breakdown']['content']}/30")
            with col4:
                st.metric("Link Health", f"{score_data['breakdown']['links']}/20")
            with col5:
                st.metric("Technical", f"{score_data['breakdown']['technical']}/25")
                
            # Detailed Breakdown Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Meta Data", "📝 Content & Structure", "🔗 Links", "⚙️ Technical"])
            
            with tab1:
                st.subheader("Meta Tags Analysis")
                mc1, mc2 = st.columns(2)
                
                with mc1:
                    st.write("**Title Tag**")
                    if meta_res['title']:
                        st.info(f"Content: {meta_res['title']}")
                        st.write(f"Length: {meta_res['title_length']} chars (Optimal: 10-60)")
                        st.write(f"Approx Pixel Width: {meta_res['title_pixel_width']}px")
                    else:
                        st.error("Missing Title Tag")
                        
                    st.write("---")
                    st.write("**Meta Description**")
                    if meta_res['description']:
                        st.info(f"Content: {meta_res['description']}")
                        st.write(f"Length: {meta_res['description_length']} chars (Optimal: 50-160)")
                    else:
                        st.error("Missing Meta Description")
                
                with mc2:
                    st.write("**Canonical URL**")
                    if meta_res['canonical']:
                        if meta_res['canonical'] == final_url:
                            st.success(f"Correct: {meta_res['canonical']}")
                        else:
                            st.warning(f"Mismatch: {meta_res['canonical']}")
                    else:
                        st.warning("Missing Canonical Tag")
                        
                    st.write("---")
                    st.write("**Robots & Favicon**")
                    st.write(f"Robots Meta: `{meta_res['robots'] if meta_res['robots'] else 'None'}`")
                    st.write(f"Favicon: {'✅ Found' if meta_res['favicon'] else '❌ Missing'}")

            with tab2:
                st.subheader("Content Structure")
                
                st.write(f"**Word Count:** {content_res['word_count']} (Visible words)")
                
                col_h1, col_kw = st.columns(2)
                with col_h1:
                    st.write("**Heading Structure**")
                    if content_res['h1_count'] == 0:
                        st.error("❌ H1 Missing")
                    elif content_res['h1_count'] > 1:
                        st.warning(f"⚠️ Multiple H1 Tags Found ({content_res['h1_count']})")
                    else:
                        st.success("✅ Single H1 Tag Found")
                        
                    with st.expander("View Text Hierarchy"):
                        for level, text in content_res['structure_hierarchy']:
                            st.write(f"**{level.upper()}**: {text}")
                            
                with col_kw:
                    st.write("**Top 5 Keywords**")
                    if content_res['top_keywords']:
                        kw_df = pd.DataFrame(content_res['top_keywords'], columns=['Keyword', 'Frequency'])
                        st.dataframe(kw_df, hide_index=True)
                    else:
                        st.write("No significant keywords found.")

                st.write("---")
                st.write("**Image Analysis**")
                st.write(f"Total Images: {content_res['total_images']}")
                st.write(f"Missing ALT Tags: {content_res['missing_alt']}")
                
                if content_res['missing_alt'] > 0:
                    with st.expander("Show Images Missing Alt Text"):
                        missing_imgs = [img for img in content_res['image_details'] if not img['has_alt']]
                        st.dataframe(pd.DataFrame(missing_imgs)[['src']], hide_index=True)

            with tab3:
                st.subheader("Link Analysis")
                st.write(f"**Internal:** {link_res['internal_count']} | **External:** {link_res['external_count']} | **Total:** {link_res['total_links']}")
                
                st.write("**Health Check (First 20 Links)**")
                if link_res['details']:
                    df_links = pd.DataFrame(link_res['details'])
                    
                    def status_color(val):
                        if val == 200: return 'background-color: #90ee90'
                        elif val >= 400 or val == 0: return 'background-color: #ffcccb'
                        elif val >= 300: return 'background-color: #ffebcd'
                        return ''
                        
                    st.dataframe(df_links.style.map(status_color, subset=['status']))
                else:
                    st.info("No links found on page.")

            with tab4:
                st.subheader("Technical Performance")
                
                tp1, tp2, tp3 = st.columns(3)
                with tp1:
                    st.metric("Response Time", f"{tech_res['response_time']} ms")
                with tp2:
                    is_https = tech_res['https']
                    st.metric("HTTPS Encryption", "Secure" if is_https else "Insecure", delta="✅" if is_https else "❌", delta_color="normal")
                with tp3:
                    is_mobile = tech_res['mobile_friendly']
                    st.metric("Mobile Viewport", "Present" if is_mobile else "Missing", delta="✅" if is_mobile else "❌", delta_color="normal")
