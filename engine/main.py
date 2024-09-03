"""
Main python code of engine
"""
import re
import requests
from bs4 import BeautifulSoup


def is_valid_cve_id(cve_id):
    """
    Checks given input against regex if it is valid returns true, otherwise false.
    """
    # Regex of CVE-ID
    cve_pattern = r'^CVE-\d{4}-\d{4,}$'

    # Match case
    match = re.match(cve_pattern, cve_id)

    # Return boolean of match
    return bool(match)


def check_cve_on_website(cve_id):
    websites = [
        f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}",
        f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        f"https://www.cvedetails.com/cve/{cve_id}/",
        f"https://vulners.com/cve/{cve_id}"
        f"https://www.exploit-db.com/search?cve={cve_id}"
    ]

    returns = []

    for url in websites:
        try:
            
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()

            # Check if the CVE ID is in the text
            if "CVE ID Not Found" in page_text or "Nothing found" in page_text:
                #returns.append["False"]
                print(url, "false")
            else:
                print(url, "true")
        except requests.exceptions.RequestException as e:
            pass

    n = 0
    for i in returns:
        if i == "False":
            n += 1
    
    if n > 2:
        return False


if __name__ == "__main__":
    user_input = input("Enter CVE-ID: ")
    case = is_valid_cve_id(user_input)
    print(case)
    if case:
        case1 = check_cve_on_website(input)