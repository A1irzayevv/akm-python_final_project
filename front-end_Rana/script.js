function generateReport() {
    document.getElementById('menu').classList.add('hidden');
    document.getElementById('cve-form').classList.remove('hidden');
}

function exitProgram() {
    alert('Exiting the program. Goodbye!');
    window.close();
}

function validateCVE() {
    const cveId = document.getElementById('cve-id').value.trim();
    const cveRegex = /^CVE-\d{4}-\d{4,}$/;

    if (cveRegex.test(cveId)) {
        document.getElementById('cve-form').classList.add('hidden');
        document.getElementById('format-selection').classList.remove('hidden');
    } else {
        alert('Invalid CVE ID format. Please use the format CVE-YYYY-NNNN.');
    }
}

function createReport(format) {
    const cveId = document.getElementById('cve-id').value.trim();
    let resultText = '';

    switch (format) {
        case 'docx':
            resultText = `Word report for ${cveId} is being created...`;
            break;
        case 'md':
            resultText = `Markdown report for ${cveId} is being created...`;
            break;
        case 'pdf':
            resultText = `PDF report for ${cveId} is being created...`;
            break;
    }

    document.getElementById('format-selection').classList.add('hidden');
    document.getElementById('result').textContent = resultText;
    document.getElementById('result').classList.remove('hidden');

    openReferences(cveId);
}

function openReferences(cveId) {
    const urls = [
        `https://nvd.nist.gov/vuln/detail/${cveId}`,
        `https://www.exploit-db.com/search?cve=${cveId}`,
        `https://cve.mitre.org/cgi-bin/cvename.cgi?name=${cveId}`,
        `https://vulners.com/search?query=${cveId}`,
        `https://vulmon.com/vulnerabilitydetails?qid=${cveId}`
    ];

    urls.forEach(url => {
        window.open(url, '_blank');
    });
}
