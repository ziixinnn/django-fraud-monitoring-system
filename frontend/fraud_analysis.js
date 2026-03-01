function openFraudAnalysis(alertId) {
    fetch(API.alertAnalysis(alertId), {
        credentials: "include" 
    })
        .then(res => res.json())
        .then(data => {
            renderFraudAnalysis(data);
            new bootstrap.Modal(
                document.getElementById("fraudAnalysisModal")
            ).show();
        })
        .catch(() => alert("Unable to load fraud analysis"));
}

function renderFraudAnalysis(data) {
    const body = document.getElementById("fraud-analysis-body");
    currentCustomerId = data.customer_id;

    body.innerHTML = `
        <div class="card mb-3 text-center">
            <div class="card-body">
                <canvas id="riskGauge" height="160"></canvas>
                <h6 class="mt-3">
                    Risk Level:
                    <span class="fw-bold text-danger">
                        ${data.risk_level}
                    </span>
                </h6>
            </div>
        </div>

        <div class="card mb-3">
            <div class="card-header fw-bold">Explanation</div>
            <div class="card-body">
                ${data.reason || "No explanation provided"}
            </div>
        </div>

        <div
            id="user-profile-link"
            class="card-header fw-bold text-decoration-underline text-primary"
            style="cursor:pointer;"
        >
            User Profile Details
        </div>

        <div class="d-flex justify-content-end gap-2">
            <button id="confirm-fraud-btn" class="btn btn-danger">
                Confirm Fraud
            </button>
            <button id="false-positive-btn" class="btn btn-success">
                False Positive
            </button>
            <button id="pending-btn" class="btn btn-secondary">
                Mark as Pending
            </button>
        </div>
    `;

    drawGauge(data.risk_thresholds, data.risk_score);

    document
        .getElementById("confirm-fraud-btn")
        .addEventListener("click", () =>
            handleAction(currentTransactionId, "CONFIRM_FRAUD")
        );

    document
        .getElementById("false-positive-btn")
        .addEventListener("click", () =>
            handleAction(currentTransactionId, "FALSE_POSITIVE")
        );

    document
        .getElementById("pending-btn")
        .addEventListener("click", () =>
            handleAction(currentTransactionId, "MARK_AS_PENDING")
        );

    document
    .getElementById("user-profile-link")
    .addEventListener("click", () => {
        if (!currentCustomerId) {
            alert("Missing customer");
            return;
        }
        loadCustomerProfileView(currentCustomerId);
    });

}

function drawGauge(thresholds, riskScore) {
    const ctx =
        document.getElementById("riskGauge").getContext("2d");

    const levels = Object.entries(thresholds)
        .sort((a, b) => a[1] - b[1]);

    const segments = [];
    let prev = 0;

    levels.forEach(([_, value]) => {
        segments.push(value - prev);
        prev = value;
    });
    segments.push(1 - prev);

    new Chart(ctx, {
        type: "doughnut",
        data: {
            datasets: [{
                data: segments,
                backgroundColor: [
                    "#198754",
                    "#0d6efd",
                    "#ffc107",
                    "#fd7e14",
                    "#dc3545"
                ]
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            cutout: "70%",
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        },
        plugins: [{
            id: "needle",
            afterDraw(chart) {
                if (typeof riskScore !== "number") return;

                const meta = chart.getDatasetMeta(0).data[0];
                const angle =
                    (-Math.PI / 2) + (riskScore * Math.PI);

                const ctx = chart.ctx;
                ctx.save();
                ctx.translate(meta.x, meta.y);
                ctx.rotate(angle);
                ctx.beginPath();
                ctx.moveTo(0, 0);
                ctx.lineTo(0, -meta.outerRadius + 8);
                ctx.lineWidth = 3;
                ctx.stroke();
                ctx.restore();
            }
        }]
    });
}

async function postTransactionAction(transactionId, action) {
    const res = await fetch(API.postTransactionAction(transactionId), {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ action })
    });
    if (!res.ok) throw new Error("Action failed");
    return await res.json();
}

function handleAction(transactionId, action) {
    if (!transactionId) return alert("Missing transaction id");

    postTransactionAction(transactionId, action)
        .then(() => {
            bootstrap.Modal
                .getInstance(
                    document.getElementById("fraudAnalysisModal")
                )
                .hide();

            loadAlertData("pending");
        })
        .catch(() => alert("Failed to submit action"));
}
