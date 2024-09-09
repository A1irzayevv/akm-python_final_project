import re
import os
import datetime
import requests
from exploit import *
from dotenv import load_dotenv
load_dotenv()


def Validator(cveId):
    cveRegex = r'^CVE-\d{4}-\d{4,8}$'
    if re.match(cveRegex, cveId):
        if cveId.split("-")[1].isdigit():
            yearInCVE = int(cveId.split("-")[1])
            yearNow = datetime.datetime.now().year
            if yearInCVE < 1999:
                return "Error: (YEAR_LOW)"
            elif yearInCVE > yearNow:
                return "Error: (YEAR_HIGH)"
            else:
                return ValidatorID(cveId)
    else:
        return "Error: (INCORRECT_INPUT)"

def ValidatorID(cveId):
    mitreUrl = f'https://cveawg.mitre.org/api/cve/{cveId}'
    mitreResponse = requests.get(mitreUrl)
    mitreData = mitreResponse.json()
    if "error" in mitreData.keys():
        return "Error: (CVE_NOT_EXIST_OR_RESERVED)"
    return False

def fetchData(cveId):
    nvd_api_key = os.getenv("NVD_API_KEY")
    nistUrl = f'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cveId}'
    headers = {"apiKey": nvd_api_key,}
    mitreUrl = f'https://cveawg.mitre.org/api/cve/{cveId}'
    mitreResponse = requests.get(mitreUrl)
    nistResponse = requests.get(nistUrl, headers=headers)

    if mitreResponse.status_code == 200 and nistResponse.status_code == 200:
        mitreData = mitreResponse.json()
        nistData = nistResponse.json()
        references = []

        description = nistData["vulnerabilities"][0]["cve"]["descriptions"][0].get("value", "N/A")

        for reference in nistData["vulnerabilities"][0]["cve"]["references"]:
            if "tags" in reference and "Broken Link" in reference["tags"]:
                continue
            elif ("tags" in reference and "Exploit" in reference["tags"]) or reference["url"].startswith("https://www.exploit-db.com"):
                references.append(reference["url"])
        if len(references) == 0:
            references = ["N/A"]

        if len(nistData["vulnerabilities"][0]["cve"]["metrics"]) > 0:
            if list(nistData["vulnerabilities"][0]["cve"]["metrics"].keys())[0].startswith("cvssMetricV3"):
                key = list(nistData["vulnerabilities"][0]["cve"]["metrics"].keys())[0]
                CVSSData = nistData["vulnerabilities"][0]["cve"]["metrics"][key][0]["cvssData"]
                severity = CVSSData.get("baseSeverity", "N/A")
                score = CVSSData.get("baseScore", "N/A")
                conf = CVSSData.get("confidentialityImpact", "N/A")
                integ = CVSSData.get("integrityImpact", "N/A")
                aviab = CVSSData.get("availabilityImpact", "N/A")
                vector = CVSSData.get("attackVector", "N/A")

            elif "cvssMetricV2" in nistData["vulnerabilities"][0]["cve"]["metrics"]:
                CVSSData = nistData["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]
                severity = nistData["vulnerabilities"][0]["cve"]["metrics"]["cvssMetricV2"][0].get("baseSeverity", "N/A")
                score = CVSSData.get("baseScore", "N/A")
                conf = CVSSData.get("confidentialityImpact", "N/A")
                integ = CVSSData.get("integrityImpact", "N/A")
                aviab = CVSSData.get("availabilityImpact", "N/A")
                vector = CVSSData.get("attackVector", "N/A")
        else:
            CVSSData = {}
            severity = "Not determined"
            score = "N/A"

        if mitreData["containers"]["cna"]["affected"] and mitreData["containers"]["cna"]["affected"][0]:
            vendor = mitreData["containers"]["cna"]["affected"][0].get("vendor", "N/A")
            product = mitreData["containers"]["cna"]["affected"][0].get("product", "N/A")

        requiredData = {
            "CVE ID": cveId,
            "Score": score,
            "Severity": severity,
            "CVSS Vector": CVSSData.get("vectorString", "N/A"),
            "Description": description,
            "confidentialityImpact": conf,
            "integrityImpact": integ,
            "availabilityImpact": aviab,
            "attackVector": vector,
            "Vendor": vendor,
            "Product": product,
            "References":  references,
            "State": mitreData["cveMetadata"].get("state", "N/A"),
            "Exploits": exploit_scraper(cveId),
        }

        if "tags" in mitreData["containers"]["cna"] and mitreData["containers"]["cna"]["tags"][0] == "disputed":
            requiredData["State of ID"] = "DISPUTED"

        return requiredData

    else:
        return "Error: (DATA_FETCH_FAILURE)"