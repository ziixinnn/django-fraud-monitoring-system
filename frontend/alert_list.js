
function truncate(text, max = 40) {
    if (!text) return "-";
    return text.length > max ? text.slice(0, max) + "…" : text;
}

function loadAlertData(view = "pending") {
    const tbody = document.getElementById("alert_table-body");
    tbody.innerHTML = "";

    fetch(API.alertList(view), {
        credentials: "include"  
    })
        .then(r => r.json())
        .then(data => {
            data.forEach(item => {
                const tr = document.createElement("tr");
                
                const shortReason = truncate(item.reason, 40);
                
                tr.innerHTML = `
                    <td>${item.timestamp}</td>
                    <td>${item.transaction}</td>
                    <td>${item.amount}</td>
                    <td>${item.location}</td>
                    <td>${item.risk_score ?? "-"}</td>
                    <td>${item.risk_level ?? "-"}</td>
                    <td title="${item.reason || ""}">
                        ${shortReason}
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            ${view === "resolved" ? "View" : "Review"}
                        </button>
                    </td>
                `;

                tr.querySelector("button").onclick = () =>
                    view === "resolved"
                        ? viewResolvedDetail(item.alert_id)
                        : viewAlertDetail(item.alert_id);

                tbody.appendChild(tr);
            });
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-view]").forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll("[data-view]").forEach(b =>
                b.classList.replace("btn-primary", "btn-outline-primary")
            );
            btn.classList.replace("btn-outline-primary", "btn-primary");
            loadAlertData(btn.dataset.view);
        };
    });

    loadAlertData("pending");
});