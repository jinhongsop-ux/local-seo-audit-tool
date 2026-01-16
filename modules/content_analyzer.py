from bs4 import BeautifulSoup
from collections import Counter
import re
from stop_words import get_stop_words

def analyze_content(soup):
    """
    Analyzes content structure: Headings, Word Count, Keywords, Images.
    Uses 'stop-words' package to avoid NLTK dependency issues.
    """
    results = {}
    
    # 1. Headings Analysis
    headings = {}
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    all_headings = []
    
    for h in heading_tags:
        tags = soup.find_all(h)
        headings[h] = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
        for tag in tags:
            if tag.get_text(strip=True):
                all_headings.append((h, tag.get_text(strip=True)))
                
    results['headings'] = headings
    results['h1_count'] = len(headings['h1'])
    results['structure_hierarchy'] = all_headings

    # 2. Word Count (Visible Text)
    # Remove scripts and styles
    for script in soup(["script", "style"]):
        script.extract()
        
    text = soup.get_text(separator=' ')
    words = re.findall(r'\b\w+\b', text.lower())
    results['word_count'] = len(words)
    
    # 3. Keyword Analysis (TF-IDF style frequency)
    try:
        stop_words = set(get_stop_words('en'))
        # Add some common web terms to stop words
        stop_words.update(['copyright', 'rights', 'reserved', 'contact', 'home', 'privacy', 'policy'])
        
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2 and not w.isdigit()]
        word_freq = Counter(filtered_words)
        results['top_keywords'] = word_freq.most_common(5)
    except Exception as e:
        results['top_keywords'] = []
        print(f"Keyword analysis error: {e}")

    # 4. Image Analysis
    images = soup.find_all('img')
    img_analysis = []
    missing_alt = 0
    
    for img in images:
        src = img.get('src')
        alt = img.get('alt')
        
        if not alt:
            missing_alt += 1
            
        img_analysis.append({
            'src': src,
            'alt': alt,
            'has_alt': bool(alt)
        })
        
    results['total_images'] = len(images)
    results['missing_alt'] = missing_alt
    results['image_details'] = img_analysis
    
    return results
