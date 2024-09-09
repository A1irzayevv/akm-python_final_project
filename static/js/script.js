document.addEventListener("DOMContentLoaded", function () {
    // Color the score circle based on value
    const scoreCircle = document.querySelector(".score-circle");

    if (scoreCircle) {
        const score = parseFloat(scoreCircle.getAttribute("data-score"));
        if (!isNaN(score)) {
            if (score < 4.0) {
                scoreCircle.classList.add("low");  // Green for low severity
            } else if (score < 7.0) {
                scoreCircle.classList.add("medium");  // Orange for medium severity
            } else if (score <= 10.0) {
                scoreCircle.classList.add("high");  // Red for high severity
            } else {
                scoreCircle.classList.add("unknown");  // Grey if unknown
            }
        } else {
            scoreCircle.classList.add("unknown");  // Grey if not a number
        }
    }

    // Focus button functionality
    const focusButton = document.getElementById('focusButton');
    const input = document.getElementById('userInput');

    focusButton.addEventListener('click', function () {
        input.focus();

        if (!focusButton.classList.contains('delete-button')) {
            focusButton.classList.add('delete-button');
            focusButton.textContent = 'DELETE!';
        } else {
            focusButton.classList.remove('delete-button');
            focusButton.textContent = 'PUSH!';
            input.value = '';
        }
    });

    // Update severity based on severity paragraph content
    const severityParagraph = document.getElementById("severity");

    if (severityParagraph) {
        const severityValue = severityParagraph.textContent;
        updateSeverity(severityValue);
    }

    function updateSeverity(sevValue) {
        const sevValueNumber = Number(sevValue.split(" ")[0]);
        severityParagraph.textContent = `Severity: ${sevValue}`;

        severityParagraph.classList.remove('low-severity', 'medium-severity', 'high-severity');

        if (sevValueNumber < 4) {
            severityParagraph.classList.add('low-severity');
        } else if (sevValueNumber >= 4 && sevValueNumber <= 7) {
            severityParagraph.classList.add('medium-severity');
        } else {
            severityParagraph.classList.add('high-severity');
        }
    }
});
