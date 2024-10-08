import webbrowser
import random
import requests


# Rahim Sadigov - checks if url is valid, then if yes, opens it in new tab.
def is_link_valid(url):
    """Check links if it is valid by sending request

    Args:
        url (str): url to check by finction

    Returns:
        Boolean: True if link valid, False if link is broken
    """    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Use requests.get with allow_redirects=True to follow redirects
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        # Normally, I will only leave status_code 200 as allowed. But shitty Microsoft webpages return unofficial self-made 999 response code. Hovewer if it is Microsoft page it will open normally even it returns 999.
        return (response.status_code == 200) or (response.status_code == 999 and "microsoft" in url)
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
