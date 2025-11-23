// Login direct redirect (no validation for now)
function loginRedirect() {
    window.location.href = "dashboard.html";
}

// Consent controls
let consent = {
    income: true,
    location: true,
    demographics: true,
    spending: true,
    credit: true
};

function updateConsent(type, value) {
    consent[type] = value;
}

function saveConsent() {
    const disabled = Object.values(consent).filter(v => !v).length;
    const impact = document.getElementById("consentImpact");

    if (disabled === 0) {
        impact.className = "alert alert-success";
        impact.textContent = "All enabled. AI accuracy at maximum.";
    } else {
        impact.className = "alert alert-warning";
        impact.textContent = `${disabled} data fields disabled — AI accuracy may be reduced.`;
    }
}

// Correction request from AI profile
function requestCorrection(type) {
    alert("Your correction request has been submitted for human review.");
}

// Resolve requests in admin table
function resolveRequest(btn) {
    btn.parentElement.previousElementSibling.textContent = "Resolved";
    btn.remove();
}
