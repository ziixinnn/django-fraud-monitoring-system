function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(API.staffLogin(), {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ username, password })
    })
        .then(res => res.json())
        .then(data => {
            if (data.message === "Login success") {
                window.location.href = "transaction.html";
            } else {
                alert("Login failed");
            }
        })
        .catch(() => alert("Server error"));
}

document
    .getElementById("loginBtn")
    .addEventListener("click", login);

function authGuard() {
    fetch(API.checkAuth(), {
        credentials: "include"
    })
        .then(res => {
            if (res.status === 401 || res.status === 403) {
                window.location.href = "login.html";
            }
        })
        .catch(() => {
            window.location.href = "login.html";
        });
}