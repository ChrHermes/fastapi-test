// index.js
import { showModal, showUpdateModal, showUserCommentModal, showDatabaseResetModal } from './modal.js';

/* =====================================
   GLOBALE FUNKTIONEN FÜR LOGGING & UI
===================================== */

/**
 * Lädt die Logs per API-Call und ruft displayLogs auf.
 */
async function fetchLogs() {
    try {
        const response = await fetch("/logs");
        const data = await response.json();
        displayLogs(data.logs);
    } catch (error) {
        console.error("Fehler beim Laden der Logs:", error);
    }
}

/**
 * Zeigt die Logs im Log-Container an.
 */
function displayLogs(logs) {
    const logContainer = document.getElementById("log");
    logContainer.innerHTML = "";
    const selectedLevel = document.getElementById("log-level").value;
    logs.forEach(log => {
        if (selectedLevel === "ALL" || log.level === selectedLevel) {
            const logEntry = document.createElement("div");
            logEntry.textContent = `${log.timestamp} [${log.level}] ${log.message}`;
            logContainer.appendChild(logEntry);
        }
    });
    logContainer.scrollTop = logContainer.scrollHeight;
}

/**
 * Wrapper-Funktion zum Laden der Logs.
 */
function loadLogs() {
    fetchLogs();
}

/**
 * Sendet einen einfachen POST-Request an die angegebene URL.
 * Bei Erfolg werden die Logs neu geladen.
 */
async function sendPostRequest(url) {
    try {
        const response = await fetch(url, { method: "POST" });
        if (!response.ok) {
            console.error("Fehler beim Senden der Anfrage:", response.statusText);
        } else {
            loadLogs();
        }
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

/**
 * Passt die Breite des Containers dynamisch an.
 */
// function updateContainerWidth() {
//     const container = document.querySelector(".container");
//     if (container) {
//         container.style.setProperty("--container-width", container.clientWidth + "px");
//     }
// }

// Initiale Anpassung der Container-Größe und Log-Container
// window.addEventListener("load", () => {
//     const logContainer = document.querySelector(".log-container");
//     if (logContainer) {
//         logContainer.style.width = logContainer.clientWidth + "px";
//         logContainer.style.height = logContainer.clientHeight + "px";
//     }
//     updateContainerWidth();
// });

// window.addEventListener("resize", updateContainerWidth);

/* =====================================
         EVENT LISTENER INITIALISIERUNG
===================================== */
document.addEventListener("DOMContentLoaded", () => {
    // Logs initial laden
    loadLogs();

    // Log-Level wechseln: Neue Logs laden
    document.getElementById("log-level").addEventListener("change", fetchLogs);

    // Button: Datenbank-Reset
    document.getElementById("btnDatabaseReset").addEventListener("click", () => {
        // showDatabaseResetModal ruft intern den API-Call zum Abrufen der DB-Infos auf
        showDatabaseResetModal(loadLogs);
    });

    // Button: Software-Updates prüfen
    document.getElementById("btnUpdateSoftware").addEventListener("click", showUpdateModal);

    /**
     * Initialisiert den Event-Listener für den Button zum Hinzufügen eines Benutzerkommentars.
     * Beim Klick wird showUserCommentModal aufgerufen, wobei loadLogs als Callback übergeben wird,
     * damit die Logs nach dem Hinzufügen aktualisiert werden.
     */
    document.getElementById("btnAddNote").addEventListener("click", () => {
        showUserCommentModal(loadLogs);
    });

    // Weitere Buttons, die direkte POST-Anfragen senden:
    document.getElementById("btnReboot").addEventListener("click", () => sendPostRequest("/system/reboot"));
    document.getElementById("btnShutdown").addEventListener("click", () => sendPostRequest("/system/shutdown"));

    // Logout-Button: Logout durchführen und zur Login-Seite navigieren
    document.getElementById("logoutButton").addEventListener("click", async () => {
        await fetch("/logout", { method: "GET" });
        window.location.href = "/login";
    });
});
