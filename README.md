# 🔍 Local SEO Audit Tool (Python + Playwright)

A powerful, locally-hosted SEO audit tool built with **Python** and **Streamlit**. Unlike standard scrapers, this tool uses **Playwright** (Headless Browser) to render JavaScript, ensuring it can analyze modern websites (SPA, React, Vue) just like a real user.

这是一个基于 **Python** 和 **Streamlit** 构建的强大本地 SEO 审计工具。与普通爬虫不同，本工具使用 **Playwright**（无头浏览器）来渲染 JavaScript，确保能够像真实用户一样分析现代网站（SPA, React, Vue）。

---

## ✨ Features (功能特性)

* **🕵️‍♂️ Stealth Mode (隐身模式):** Bypasses 403 Forbidden & anti-bot protections using advanced browser fingerprinting evasion. (能绕过 403 禁止访问和反爬虫防火墙)
* **⚡ JavaScript Rendering:** Fully renders the DOM before analysis, capturing content dynamically loaded by JS. (完整渲染 DOM，抓取动态加载内容)
* **📊 Comprehensive Audit (全方位审计):**
    * **Meta Data:** Title, Description, Canonical tag, Favicon presence.
    * **Content:** H1-H6 hierarchy check, Word count, Keyword frequency (TF-IDF), Image Alt attribute analysis.
    * **Links:** Internal vs External link breakdown, **Concurrent** health check (Status 200/404) for speed.
    * **Technical:** Response time, HTTPS check, Mobile Viewport detection.
* **🚀 High Performance:** Uses `ThreadPoolExecutor` for fast link checking and optimized Playwright lifecycle management.
* **🔒 Privacy Focused:** Runs 100% locally. Your data and target URLs never leave your machine. (100% 本地运行，数据隐私安全)

---

## 🛠️ Installation (安装指南)

### Prerequisites (前置要求)
* **Python 3.10 - 3.12** (⚠️ Note: Python 3.14 is currently NOT supported due to asyncio incompatibility)
* Git

### Step 1: Clone the Repository (克隆仓库)
```bash
git clone [https://github.com/YOUR_USERNAME/local-seo-audit-tool.git](https://github.com/YOUR_USERNAME/local-seo-audit-tool.git)
cd local-seo-audit-tool