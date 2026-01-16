import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_status_code(url, timeout=5):
    """Checks the HTTP status code of a single URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; SEOAuditTool/1.0)'}
        response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        if response.status_code == 405: # Method Not Allowed, try GET
            response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        return response.status_code
    except requests.exceptions.Timeout:
        return 408
    except requests.exceptions.RequestException:
        return 0 # Error

def analyze_links(soup, base_url, max_links_to_check=20):
    """
    Extracts and analyzes links from the page.
    Uses ThreadPoolExecutor for parallel status code checking.
    """
    links_data = []
    internal_count = 0
    external_count = 0
    
    base_domain = urlparse(base_url).netloc
    
    all_tags = soup.find_all('a', href=True)
    
    unique_links = set()
    links_to_check = []
    
    for tag in all_tags:
        href = tag.get('href').strip()
        if not href or href.startswith(('javascript:', 'mailto:', 'tel:', '#')):
            continue
            
        full_url = urljoin(base_url, href)
        
        # Deduplication for checking list
        if full_url not in unique_links:
            unique_links.add(full_url)
            
            is_internal = False
            link_domain = urlparse(full_url).netloc
            
            if not link_domain: # Relative link
                is_internal = True
            elif link_domain == base_domain or link_domain.endswith('.' + base_domain):
                is_internal = True
            
            if is_internal:
                internal_count += 1
            else:
                external_count += 1
                
            links_data.append({
                'url': full_url,
                'text': tag.get_text(strip=True)[:50],
                'type': 'Internal' if is_internal else 'External',
                'status': None # To be filled
            })

    # Select top N unique links to check status for performance
    check_list = links_data[:max_links_to_check]
    
    # Parallel Execution
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(get_status_code, item['url']): item for item in check_list}
        
        for future in as_completed(future_to_url):
            item = future_to_url[future]
            try:
                status = future.result()
                item['status'] = status
            except Exception:
                item['status'] = 0

    return {
        'internal_count': internal_count,
        'external_count': external_count,
        'total_links': len(links_data),
        'details': check_list # Return the checked ones with status
    }
