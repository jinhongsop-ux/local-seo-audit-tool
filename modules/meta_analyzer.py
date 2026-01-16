from bs4 import BeautifulSoup

def analyze_meta(soup, current_url):
    """
    Analyzes SEO Meta Tags: Title, Description, Canonical, Robots, Favicon.
    """
    results = {}
    
    # 1. Title Tag
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        title = title_tag.string.strip()
        results['title'] = title
        results['title_length'] = len(title)
        # Approx pixel width (Arial 16px approx) - very rough estimate
        results['title_pixel_width'] = len(title) * 8 
    else:
        results['title'] = None
        results['title_length'] = 0
        results['title_pixel_width'] = 0
        
    # 2. Meta Description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag and desc_tag.get('content'):
        desc = desc_tag.get('content').strip()
        results['description'] = desc
        results['description_length'] = len(desc)
    else:
        results['description'] = None
        results['description_length'] = 0
        
    # 3. Canonical Tag
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    if canonical_tag and canonical_tag.get('href'):
        results['canonical'] = canonical_tag.get('href').strip()
    else:
        results['canonical'] = None
        
    # 4. Robots Meta
    robots_tag = soup.find('meta', attrs={'name': 'robots'})
    if robots_tag and robots_tag.get('content'):
        results['robots'] = robots_tag.get('content').strip()
    else:
        results['robots'] = None
        
    # 5. Favicon
    favicon_tag = soup.find('link', attrs={'rel': 'icon'}) or soup.find('link', attrs={'rel': 'shortcut icon'})
    if favicon_tag and favicon_tag.get('href'):
        results['favicon'] = favicon_tag.get('href').strip()
    else:
        results['favicon'] = None
        
    return results
