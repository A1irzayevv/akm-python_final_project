import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the Generative AI model with API key
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def return_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response

def response_ai(cve_id):
    prompt = f"""
    You are a cybersecurity assistant tasked with gathering detailed and accurate information about a given CVE (Common Vulnerabilities and Exposures) ID. Your job is to provide a human-friendly explanation of the vulnerability, its potential impact, and the recommended proactive measures or protections against it. Your response should be structured and easy to understand, even for those without a deep technical background.

    Here is the CVE ID: {cve_id}

    Instructions:
    Be very precise!!! (Don't generate unrelated text to given CVE ID)
    Identify the CVE:

    Use trusted sources (NVD, MITRE, security advisories, etc.) to gather a full description of the CVE.
    Include key details like affected software/hardware, attack vectors, and potential risks and dont include CVSS score because it can be unaccurate.
    Explain the Vulnerability in Simple Terms:

    Describe how the vulnerability works in a way that non-experts can understand. Avoid excessive technical jargon, and focus on the core issue.
    Example: “This vulnerability allows attackers to access sensitive data because of a flaw in how the software handles encryption keys.”
    Impact on Systems:

    Describe the possible impact of the CVE on an organization's system. For instance, can it lead to data breaches, unauthorized access, or disruption of services?
    Proactive Measures and Protection:

    Offer clear, actionable steps that users or organizations can take to mitigate the risk from this vulnerability.
    Mention updates, patches, security configurations, or best practices that should be applied.
    For example: “To protect your systems, ensure you update to version X, as it contains a patch for this flaw.”
    Broader Cybersecurity Context:

    Briefly explain why proactive security is crucial in general.
    Mention any relevant industry standards (e.g., applying regular patches, employing firewalls, educating staff on phishing tactics) to help users better secure their systems.
    Conclusion:

    Summarize the key points: What is the vulnerability, why it’s dangerous, and what steps should be taken immediately.
    Reassure users that by following the suggested measures, they can significantly reduce their risk.

    Example of a Response:

    CVE-2024-XXXX - Summary:

    Vulnerability Overview: CVE-XXXX-XXXX is a critical vulnerability in [software name], which allows an attacker to gain unauthorized remote access to your system by exploiting a flaw in how the application handles network connections. The vulnerability has a CVSS score of 9.8, making it highly severe, and affects versions [X.Y] to [X.Z].

    In Simple Terms: Imagine that the software you’re using has a weak lock on its front door. An attacker can easily pick this lock and get into your system, potentially accessing sensitive files or taking control of your entire network.

    Potential Impact: If left unaddressed, this vulnerability could allow cybercriminals to steal data, disrupt business operations, or even spread malware across your network. Once exploited, the attacker could perform malicious activities without detection.

    Proactive Measures:

    Patch your system: Ensure you update to version [X.Z.1], which has been released by the vendor to fix this flaw.
    Restrict network access: Limit exposure to external networks, use a VPN, and configure your firewall to block unauthorized access attempts.
    Monitor traffic: Implement network monitoring tools to detect any unusual activity that might indicate an attempted exploitation.
    Regular updates: Establish a routine patching schedule to reduce the risk of future vulnerabilities.
    Broader Security Practice: Beyond this specific CVE, maintaining a strong cybersecurity posture is essential. This includes educating your team about phishing attacks, enforcing multi-factor authentication (MFA), and regularly reviewing system configurations to ensure they align with industry best practices.
    """

    answer = return_gemini_response(prompt)
    return answer_editor(answer.text)

def answer_editor(cve_report):
    # Replace markdown-like headers with HTML headers
    cve_report = cve_report.replace('## ', '<h2>').replace(' - Summary:', '</h2><h3>Summary:</h3>')
    
    # List of subheadings that need to be bolded
    subheadings = [
        'Vulnerability Overview:', 
        'In Simple Terms:', 
        'Potential Impact:', 
        'Proactive Measures:', 
        'Broader Security Practice:'
    ]
    
    # Bold specific subheadings
    for heading in subheadings:
        cve_report = cve_report.replace(f'**{heading}**', f'<strong>{heading}</strong>')
    
    # Handle bold text correctly (Only subheadings will be bolded)
    # Replace markdown-like bold text with HTML strong tags
    while '**' in cve_report:
        cve_report = cve_report.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
    
    # Replace lists with unordered list items and use <span> to avoid bullets
    cve_report = cve_report.replace('* ', '<span class="list-item">').replace('\n\n', '</span><br>')
    
    # Add CSS for hiding bullets
    cve_report = '<style> .list-item { display: block; } </style>' + cve_report
    
    # Replace newline characters for paragraphs
    cve_report = cve_report.replace('\n ', '<br>')
    
    return cve_report