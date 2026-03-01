function loadCustomerProfileView(customerId) {
    currentCustomerId = customerId;
    const body = document.getElementById("fraud-analysis-body");

    body.innerHTML = `
        <div class="mb-3">
            <h5 class="fw-bold">Customer Profile</h5>
        </div>

        <div class="card mb-3">
            <div class="card-body" id="customer-info">
                Loading customer info...
            </div>
        </div>

        <div class="d-flex gap-2 mb-3">
            <button class="btn btn-outline-secondary btn-sm" data-type="all">All</button>
            <button class="btn btn-outline-danger btn-sm" data-type="Expenses">Expenses</button>
            <button class="btn btn-outline-success btn-sm" data-type="Income">Income</button>
            <button class="btn btn-outline-primary btn-sm" data-type="Savings">Savings</button>
        </div>

        <div class="card">
            <div class="card-header fw-bold">
                Transaction History
            </div>
            <div class="card-body p-0">
                <table class="table table-sm mb-0">
                    <thead class="table-light">
                        <tr>
                            <th>Sender</th>
                            <th>Receiver</th>
                            <th>Amount</th>
                            <th>Status</th>
                            <th>Type</th>
                        </tr>
                    </thead>
                    <tbody id="customer-tx-body">
                        <tr>
                            <td colspan="5" class="text-center text-muted py-3">
                                Loading transactions...
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;

    fetchCustomerProfile(customerId);
    loadTx("all");

    body.querySelectorAll("[data-type]").forEach(btn => {
        btn.addEventListener("click", () => {
            loadTx(btn.dataset.type);
        });
    });
}

function fetchCustomerProfile(customerId) {
    fetch(API.customerDetail(customerId), {
        credentials: "include"  
    })
        .then(r => r.json())
        .then(d => {
            document.getElementById("customer-info").innerHTML = `
                <div class="d-flex justify-content-between">
                    <div>
                        <div class="fw-bold">${d.customer_name}</div>
                        <div class="text-muted small">
                            Joined: ${d.joined_since}
                        </div>
                    </div>
                    <div class="text-danger fw-bold">
                        Flagged: ${d.flagged_times}
                    </div>
                </div>
            `;
        });
}

function renderTransactionTable(list) {
    const body = document.getElementById("customer-tx-body");
    if (!body) return;

    body.innerHTML = "";

    if (list.length === 0) {
        body.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-3">
                    No transactions found
                </td>
            </tr>
        `;
        return;
    }

    list.forEach(tx => {
        const typeClass =
            tx.type === "Income" ? "bg-success" :
            tx.type === "Expenses" ? "bg-danger" :
            tx.type === "Savings" ? "bg-primary" :
            "bg-secondary";

        body.innerHTML += `
            <tr>
                <td>${tx.sender_acc}</td>
                <td>${tx.receiver_acc}</td>
                <td>${tx.amount}</td>
                <td>${tx.transaction_status}</td>
                <td>
                    <span class="badge ${typeClass}">
                        ${tx.type}
                    </span>
                </td>
            </tr>
        `;
    });
}

function loadTx(type) {
    let url = API.customerTransactions(currentCustomerId);

    if (type !== "all") {
        url += `?type=${type}`;
    }

    fetch(url, {
        credentials: "include"   
    })
        .then(res => {
            if (res.status === 401 || res.status === 403) {
                window.location.href = "login.html";
                return;
            }
            return res.json();
        })
        .then(renderTransactionTable);
}
