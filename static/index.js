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

/* ---------------------------------------------- LOGOUT */
document.getElementById("logoutButton").addEventListener("click", async function() {
    await fetch("/logout", { method: "GET" });
    window.location.href = "/login";
});

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