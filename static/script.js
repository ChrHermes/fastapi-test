/* ---------------------------------------------- EVENT LISTENER */
document.addEventListener("DOMContentLoaded", function () {
    loadLogs();

    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    const logContainer = document.getElementById("log");

    document.getElementById("btnGC").addEventListener("click", function () {
        modal.classList.add("active");
        overlay.classList.add("active");
        inputField.value = "";
        inputField.focus();
    });

    cancelButton.addEventListener("click", function () {
        modal.classList.remove("active");
        overlay.classList.remove("active");
    });

    confirmButton.addEventListener("click", async function () {
        if (inputField.value === "db-reset") {
            await sendRequest("/log/button1");
            modal.classList.remove("active");
            overlay.classList.remove("active");
        } else {
            alert("Falscher Bestätigungscode!");
        }
    });
});

/* ---------------------------------------------- LOGIN */
async function sendRequest(endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { 'Authorization': 'Basic ' + btoa('admin:password') }
        });
        const data = await response.json();
        appendLog(data.message);
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        window.location.href = "/static/index.html";
    } else {
        document.getElementById("error-message").innerText = data.detail;
    }
});

/* ---------------------------------------------- THEME */
document.getElementById("theme-toggle").addEventListener("click", function () {
    const isDark = document.body.classList.toggle("dark-mode");
    localStorage.setItem("theme", isDark ? "dark" : "light");
    this.textContent = isDark ? "🌞" : "🌚";
});

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    document.getElementById("theme-toggle").textContent = "🌞";
}

/* ---------------------------------------------- LOGGING */
function appendLog(message) {
    const logContainer = document.getElementById("log");
    const timestamp = new Date().toLocaleString();
    logContainer.innerHTML += `<div class="log-entry"><span class="timestamp">[${timestamp}]</span> ${message}</div>`;
    logContainer.scrollTop = logContainer.scrollHeight;
    saveLogToServer(message);
}

async function loadLogs() {
    try {
        const response = await fetch("/logs", { method: "GET" });
        const data = await response.json();
        data.logs.forEach(msg => appendLog(msg));
    } catch (error) {
        console.error("Fehler beim Laden der Logs:", error);
    }
}

async function saveLogToServer(message) {
    // try {
    //     await fetch("/save-log", {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ message })
    //     });
    // } catch (error) {
    //     console.error("Fehler beim Speichern des Logs:", error);
    // }
}

