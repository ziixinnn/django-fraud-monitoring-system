
function renderTransactionRow(tx) {
    const statusClass =
        tx.fraud_status === "Suspicious"
            ? "badge bg-danger"
            : "badge bg-success";

    const tr = document.createElement("tr");
    tr.id = tx.transaction_id;

    tr.innerHTML = `
        <td>${tx.transaction_id}</td>
        <td>${tx.amount}</td>
        <td>${tx.timestamp}</td>
        <td>${tx.location}</td>
        <td>
            <span class="${statusClass}">
                ${tx.fraud_status}
            </span>
        </td>
        <td>
            <button class="btn btn-sm btn-outline-primary view-btn">
                View
            </button>
        </td>
    `;

    tr.querySelector(".view-btn")
        .addEventListener("click", () =>
            viewDetail(tx.transaction_id)
        );

    return tr;
}

function loadData() {
    const tbody = document.getElementById("table-body");

    fetch(API.transactionList(), { credentials: "include" })
        .then(res => res.json())
        .then(data => {
            tbody.innerHTML = "";

            data.forEach(tx => {
                const tr = renderTransactionRow(tx);
                tbody.appendChild(tr);
            });
        })
        .catch(() => {
            tbody.innerHTML =
                `<tr><td colspan="6" class="text-center text-danger">Failed to load</td></tr>`;
        });
}

function viewDetail(id) {
    fetch(API.transactionDetail(id), {
        credentials: "include" 
    })
        .then(res => res.json())
        .then(showDetail);
}

function showDetail(tx) {
    const container = document.getElementById("tx-detail");

    container.innerHTML = `
        <table class="table table-sm">
            <tr><th>ID</th><td>${tx.transaction_id}</td></tr>
            <tr><th>Amount</th><td>${tx.amount}</td></tr>
            <tr><th>Time</th><td>${tx.timestamp}</td></tr>
            <tr><th>Location</th><td>${tx.location}</td></tr>
            <tr><th>Device</th><td>${tx.device_info || "-"}</td></tr>
            <tr><th>Type</th><td>${tx.transaction_type}</td></tr>
            <tr><th>Status</th><td>${tx.transaction_status}</td></tr>
            <tr>
                <th>Fraud</th>
                <td>
                    <span class="badge ${
                        tx.fraud_status === "Suspicious" ? "bg-danger" : "bg-success"
                    }">
                        ${tx.fraud_status}
                    </span>
                </td>
            </tr>
        </table>
    `;

    new bootstrap.Modal(document.getElementById("txModal")).show();
}

loadData();

const socket = new WebSocket("ws://127.0.0.1:8000/ws/transaction/");

socket.onopen = () => {
    console.log("WebSocket connected");
};

socket.onmessage = (event) => {
    const tx = JSON.parse(event.data);
    prependTransaction(tx);
};

socket.onerror = (err) => {
    console.error("WebSocket error", err);
};

function prependTransaction(tx) {
    const tbody = document.getElementById("table-body");
    if (!tbody) return;

    if (document.getElementById(tx.transaction_id)) return;

    const tr = renderTransactionRow(tx);
    tbody.prepend(tr);
}