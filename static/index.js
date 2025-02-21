/* ---------------------------------------------- EVENT LISTENER */
document.addEventListener("DOMContentLoaded", function () {
    loadLogs();

    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    const logContainer = document.getElementById("log");
    const themeToggle = document.getElementById("theme-toggle");
    const loginForm = document.getElementById("loginForm");

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.textContent = "🌞";
    } else {
        themeToggle.textContent = "🌚";
    }

    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        themeToggle.textContent = isDark ? "🌞" : "🌚";
    });

    // document.getElementById("btnGC").addEventListener("click", function () {
    //     modal.classList.add("active");
    //     overlay.classList.add("active");
    //     inputField.value = "";
    //     inputField.focus();
    // });

    // cancelButton.addEventListener("click", function () {
    //     modal.classList.remove("active");
    //     overlay.classList.remove("active");
    // });

    // confirmButton.addEventListener("click", async function () {
    //     if (inputField.value === "db-reset") {
    //         await sendRequest("/log/button1");
    //         modal.classList.remove("active");
    //         overlay.classList.remove("active");
    //     } else {
    //         alert("Falscher Bestätigungscode!");
    //     }
    // });
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

// Automatische Umleitung zur Login-Seite, falls nicht eingeloggt
(async function checkLogin() {
    try {
        const response = await fetch("/protected");
        if (!response.ok) {
            window.location.href = "/login";
        }
    } catch (error) {
        console.error("Fehler bei der Login-Prüfung:", error);
        window.location.href = "/login";
    }
})();

// Logout-Funktion
// document.getElementById("logout-button").addEventListener("click", async function() {
//     await fetch("/logout", { method: "GET" });
//     window.location.href = "/login";
// });

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

/* ---------------------------------------------- asdf */

document.getElementById("btnGC").addEventListener("click", function () {
    modal.classList.add("active");
    overlay.classList.add("active");
    inputField.value = "";
    inputField.focus();
});

document.getElementById("cancelAction").addEventListener("click", function () {
    modal.classList.remove("active");
    overlay.classList.remove("active");
});

document.getElementById("confirmAction").addEventListener("click", async function () {
    if (inputField.value === "db-reset") {
        await sendRequest("/log/button1");
        modal.classList.remove("active");
        overlay.classList.remove("active");
    } else {
        alert("Falscher Bestätigungscode!");
    }
});
