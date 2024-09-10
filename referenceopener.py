import webbrowser
import random
import requests

def is_link_valid(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Use requests.get with allow_redirects=True to follow redirects
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def open_cve_links(cve_id, related_links):
    # Base URLs for NVD and MITRE
    nvd_url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    mitre_url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
    
    # Open NVD and MITRE links in new tabs
    webbrowser.open_new_tab(nvd_url)
    webbrowser.open_new_tab(mitre_url)

    # Create a temporary list of valid links
    valid_links = [link for link in related_links if is_link_valid(link)]
    
    # Open related links based on the length of the valid links list
    if len(valid_links) == 1:
        webbrowser.open_new_tab(valid_links[0])
    elif len(valid_links) == 2:
        webbrowser.open_new_tab(valid_links[0])
        webbrowser.open_new_tab(valid_links[1])
    elif len(valid_links) >= 3:
        random_links = random.sample(valid_links, 2)
        webbrowser.open_new_tab(random_links[0])
        webbrowser.open_new_tab(random_links[1])