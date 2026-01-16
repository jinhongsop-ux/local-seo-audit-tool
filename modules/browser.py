# 文件路径: modules/browser.py
import streamlit as st
from playwright.sync_api import sync_playwright
import time

def fetch_page_content(url):
    """
    Stealth fetcher: Hides automation flags to bypass 403/401 errors.
    """
    html_content = ""
    status_code = 0
    response_time = 0
    final_url = url
    
    try:
        with sync_playwright() as p:
            # 1. 启动浏览器时禁用 "AutomationControlled" 特征
            browser = p.chromium.launch(
                headless=False, # 保持可见，方便你观察
                args=[
                    "--disable-blink-features=AutomationControlled", 
                    "--start-maximized"
                ]
            )
            
            # 2. 伪装成最新的 Chrome 浏览器 (User-Agent)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                timezone_id="America/New_York"
            )
            
            page = context.new_page()
            
            # 3. 【关键】注入 JS，彻底抹除 navigator.webdriver 标记
            # 很多网站靠检查这个变量来抓机器人
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            start_time = time.time()
            
            try:
                # 4. 访问页面
                response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # 5. 强制等待 5 秒，让页面完全加载，也表现得像人在浏览
                page.wait_for_timeout(5000)
                
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 2)
                
                if response:
                    status_code = response.status
                    html_content = page.content()
                    final_url = response.url
                else:
                    status_code = 0
                    html_content = ""

            except Exception as nav_err:
                print(f"Navigation Error: {nav_err}")
                # 如果超时，通常也是因为被拦截了，我们当做失败处理
                return f"Blocked or Timeout: {nav_err}", 403, 0, url
            
            finally:
                page.close()
                browser.close()
                
    except Exception as e:
        return f"Browser Error: {str(e)}", 500, 0, url

    return html_content, status_code, response_time, final_url