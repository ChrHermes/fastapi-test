/* ------------------------ GLOBALE FUNKTIONEN ------------------------ */
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
    const logContainer = document.getElementById("log");
    logContainer.innerHTML = "";
    const logLevelSelect = document.getElementById("log-level");
    const selectedLevel = logLevelSelect.value;

    logs.forEach(log => {
        if (selectedLevel === "ALL" || log.level === selectedLevel) {
            // Format: "dd.mm.yyyy HH:MM:SS [LEVEL] Message"
            const logEntry = document.createElement("div");
            logEntry.textContent = `${log.timestamp} [${log.level}] ${log.message}`;
            logContainer.appendChild(logEntry);
        }
    });

    // Automatisches Scrollen nach unten
    logContainer.scrollTop = logContainer.scrollHeight;
}

function loadLogs() {
    fetchLogs();
}

async function sendRequest(url) {
    try {
        const response = await fetch(url, { method: "POST" });
        if (!response.ok) {
            console.error("Fehler beim Senden der Anfrage:", response.statusText);
        } else {
            // Aktualisiere die Logs nach erfolgreicher Anfrage
            fetchLogs();
        }
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

/* ------------------------ CONTAINER GRÖSSE ------------------------ */
function updateContainerWidth() {
    const container = document.querySelector(".container");
    if (container) {
        const width = container.clientWidth + "px";
        container.style.setProperty("--container-width", width);
    }
}

window.addEventListener("load", () => {
    const logContainer = document.querySelector(".log-container");
    logContainer.style.width = logContainer.clientWidth + "px";
    logContainer.style.height = logContainer.clientHeight + "px";
    updateContainerWidth();
});

window.addEventListener("resize", updateContainerWidth);

/* ------------------------ EVENT LISTENER & MODAL ------------------------ */
document.addEventListener("DOMContentLoaded", function () {
    loadLogs();

    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");

    document.getElementById("btnGC").addEventListener("click", function () {
        modal.classList.add("active");
        overlay.classList.add("active");
        inputField.value = "";
        inputField.focus();
        // Loggen der Anfrage zur Datenbankrücksetzung
        sendRequest("/log/db-reset");
    });  

    cancelButton.addEventListener("click", function () {
        modal.classList.remove("active");
        overlay.classList.remove("active");
    });

    confirmButton.addEventListener("click", async function () {
        if (inputField.value === "db-reset") {
            await sendRequest("/log/btnGC");
            modal.classList.remove("active");
            overlay.classList.remove("active");
        } else {
            alert("Falscher Bestätigungscode!");
        }
    });

    const logLevelSelect = document.getElementById("log-level");
    logLevelSelect.addEventListener("change", fetchLogs);

    // Initiale Logs laden
    fetchLogs();
});

/* ------------------------ LOGOUT ------------------------ */
document.getElementById("logoutButton").addEventListener("click", async function() {
    await fetch("/logout", { method: "GET" });
    window.location.href = "/login";
});
