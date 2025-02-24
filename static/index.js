/* ---------------------------------------------- EVENT LISTENER */
window.addEventListener("load", () => {
    const logContainer = document.querySelector(".log-container");
    logContainer.style.width = logContainer.clientWidth + "px";
    logContainer.style.height = logContainer.clientHeight + "px";
    updateContainerWidth();
});

window.addEventListener("resize", updateContainerWidth);

document.addEventListener("DOMContentLoaded", function () {
    loadLogs();

    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    const logContainer = document.getElementById("log");
    const logLevelSelect = document.getElementById("log-level");

    document.getElementById("btnGC").addEventListener("click", function () {
        modal.classList.add("active");
        overlay.classList.add("active");
        inputField.value = "";
        inputField.focus();
        logToServer("INFO", "Datenbankrücksetzung angefordert");
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

    async function fetchLogs() {
        try {
            const response = await fetch("/logs");
            const data = await response.json();
            displayLogs(data.logs);
        } catch (error) {
            console.error("Fehler beim Laden der Logs:", error);
        }
    }

    function displayLogs(logs) {
        logContainer.innerHTML = "";
        const selectedLevel = logLevelSelect.value;

        logs.forEach(log => {
            if (selectedLevel === "ALL" || log.level === selectedLevel) {
                const logEntry = document.createElement("div");
                logEntry.textContent = `${log.timestamp} [${log.level}] ${log.message}`;
                logContainer.appendChild(logEntry);
            }
        });
    }

    async function logToServer(level, message) {
        await fetch("/log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ level, message })
        });
        fetchLogs();
    }

    logLevelSelect.addEventListener("change", fetchLogs);
    fetchLogs();
});

/* ---------------------------------------------- LOGOUT */
document.getElementById("logoutButton").addEventListener("click", async function() {
    await fetch("/logout", { method: "GET" });
    window.location.href = "/login";
});

/* ---------------------------------------------- LOGGING */
/* Beim Laden und beim Fenster-Resize aktualisieren */
function updateContainerWidth() {
    const container = document.querySelector(".container");
    if (container) {
        const width = container.clientWidth + "px";
        container.style.setProperty("--container-width", width);
    }
}
