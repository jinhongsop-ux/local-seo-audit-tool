def calculate_score(meta_res, content_res, link_res, tech_res):
    """
    Calculates the overall SEO Health Score (0-100) based on weighted factors.
    """
    score = 0
    max_score = 100
    
    # --- 1. Meta Data (25 points) ---
    meta_score = 0
    # Title (10)
    if meta_res['title']:
        length = meta_res['title_length']
        if 10 <= length <= 60:
            meta_score += 10
        elif length > 0:
            meta_score += 5
    # Description (10)
    if meta_res['description']:
        length = meta_res['description_length']
        if 50 <= length <= 160:
            meta_score += 10
        elif length > 0:
            meta_score += 5
    # Favicon (5)
    if meta_res['favicon']:
        meta_score += 5
        
    # --- 2. Content (30 points) ---
    content_score = 0
    # H1 Presence (10)
    if content_res['h1_count'] == 1:
        content_score += 10
    elif content_res['h1_count'] > 1:
        content_score += 5 # Penalize multiple H1
        
    # Image Alt Attributes (10)
    if content_res['total_images'] > 0:
        missing_pct = content_res['missing_alt'] / content_res['total_images']
        if missing_pct == 0:
            content_score += 10
        elif missing_pct < 0.2:
            content_score += 5
        elif missing_pct < 0.5:
             content_score += 2
    else:
        content_score += 10 # No images, no problem (technically)
        
    # Content Length (10)
    if content_res['word_count'] > 600:
        content_score += 10
    elif content_res['word_count'] > 300:
        content_score += 5
        
    # --- 3. Links (20 points) ---
    link_score = 0
    # Broken Links (20) - Penalty based
    total_checked = 0
    broken = 0
    if link_res.get('details'):
        for l in link_res['details']:
            if l['status'] is not None:
                total_checked += 1
                if l['status'] >= 400 or l['status'] == 0:
                    broken += 1
    
    if total_checked > 0:
        broken_pct = broken / total_checked
        if broken_pct == 0:
            link_score += 20
        elif broken_pct < 0.1:
            link_score += 10
        elif broken_pct < 0.3:
            link_score += 5
    else:
        link_score += 20 # No links to check, assume fine
        
    # --- 4. Technical (25 points) ---
    tech_score = 0
    # HTTPS (10)
    if tech_res['https']:
        tech_score += 10
    # Mobile Friendly (10)
    if tech_res['mobile_friendly']:
        tech_score += 10
    # Response Time (5)
    if tech_res['response_time'] < 1000: # < 1s
        tech_score += 5
    elif tech_res['response_time'] < 2500: # < 2.5s
        tech_score += 2
        
    total_score = meta_score + content_score + link_score + tech_score
    
    return {
        'total': min(total_score, 100),
        'breakdown': {
            'meta': meta_score,
            'content': content_score,
            'links': link_score,
            'technical': tech_score
        }
    }
