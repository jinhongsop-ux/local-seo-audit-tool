from urllib.parse import urlparse

def analyze_technical(url, response_time, soup):
    """
    Analyzes technical SEO factors: HTTPS, Response Time, Mobile capability.
    """
    results = {}
    
    # 1. HTTPS Check
    parsed = urlparse(url)
    results['https'] = parsed.scheme == 'https'
    
    # 2. Response Time (passed from browser module)
    results['response_time'] = response_time
    
    # 3. Viewport Meta (Mobile Friendly)
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    if viewport and viewport.get('content'):
        results['viewport'] = viewport.get('content')
        results['mobile_friendly'] = True
    else:
        results['viewport'] = None
        results['mobile_friendly'] = False
        
    return results
