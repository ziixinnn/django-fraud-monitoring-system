let currentTransactionId = null;

function viewAlertDetail(id) {
    fetch(API.alertDetail(id), {
        credentials: "include"  
    })
        .then(r => r.json())
        .then(renderAlertDetail);
}

function viewResolvedDetail(id) {
    fetch(API.alertResolved(id), {
        credentials: "include"  
    })
        .then(r => r.json())
        .then(renderResolvedDetail);
}

function outcomeBadgeClass(outcome) {
    switch (outcome) {
        case "CONFIRM_FRAUD":
            return "bg-danger";   
        case "FALSE_POSITIVE":
            return "bg-info";     
        default:
            return "bg-secondary";
    }
}

function renderResolvedDetail(detail) {
    const modalEl = document.getElementById("txModal");
    const body = document.getElementById("alert-detail");

    body.innerHTML = `
        <table class="table table-sm mb-0">
            <tbody>
                <tr><th>Transaction ID</th><td>${detail.transaction}</td></tr>
                <tr><th>Amount</th><td>${detail.amount}</td></tr>
                <tr><th>Timestamp</th><td>${detail.timestamp}</td></tr>
                <tr><th>Location</th><td>${detail.location}</td></tr>
                <tr><th>Device</th><td>${detail.device_info}</td></tr>
                <tr><th>Type</th><td>${detail.transaction_type}</td></tr>
                <tr><th>Fraud Status</th><td>${detail.fraud_status}</td></tr>
                <tr>
                    <th>Resolution Time</th>
                    <td>
                        ${detail.resolution_time}
                        <span class="text-muted ms-2">
                            (Resolved in ${detail.duration})
                        </span>
                    </td>
                </tr>
                <tr>
                    <th>Outcome</th>
                    <td>
                        <span class="badge ${outcomeBadgeClass(detail.outcome)}">
                            ${detail.outcome}
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
    `;

    new bootstrap.Modal(modalEl).show();
}

function renderAlertDetail(detail) {
    currentTransactionId = detail.transaction;

    const modalEl = document.getElementById("txModal");
    const body = document.getElementById("alert-detail");

    body.innerHTML = `
        <table class="table table-sm mb-3">
            <tbody>
                <tr><th>Transaction ID</th><td>${detail.transaction}</td></tr>
                <tr><th>Amount</th><td>${detail.amount}</td></tr>
                <tr><th>Timestamp</th><td>${detail.timestamp}</td></tr>
                <tr><th>Location</th><td>${detail.location}</td></tr>
                <tr><th>Device</th><td>${detail.device_info ?? "-"}</td></tr>
                <tr><th>Type</th><td>${detail.transaction_type}</td></tr>
                <tr><th>Risk Score</th><td>${detail.risk_score}</td></tr>
                <tr><th>Status</th><td>${detail.fraud_status}</td></tr>
            </tbody>
        </table>

        <div class="text-end">
            <button id="view-analysis-btn" class="btn btn-danger btn-sm">
                View Fraud Analysis
            </button>
        </div>
    `;

    document
        .getElementById("view-analysis-btn")
        .addEventListener("click", () =>
            openFraudAnalysis(detail.alert_id)
        );

    new bootstrap.Modal(modalEl).show();
}