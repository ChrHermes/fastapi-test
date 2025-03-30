import * as modal from './modal.js';

/* =====================================
   GLOBALE FUNKTIONEN FÜR LOGGING & UI
===================================== */

/**
 * Holt die Logs von der API und ruft anschließend displayLogs auf.
 * 
 * Diese Funktion sendet eine GET-Anfrage an den Endpunkt "/logs". Nach erfolgreichem Empfang 
 * der JSON-Daten werden die Logs an displayLogs weitergegeben, um sie im UI anzuzeigen.
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
 * Zeigt die übergebenen Logs im Log-Container an.
 * 
 * Die Funktion leert zunächst den Inhalt des Log-Containers, filtert dann die Logs anhand 
 * des aktuell ausgewählten Log-Levels und fügt die passenden Einträge als neue DIV-Elemente ein.
 * Abschließend wird der Scroll-Position des Containers so gesetzt, dass der neueste Log sichtbar ist.
 *
 * @param {Array} logs - Array von Log-Objekten, wobei jedes Objekt Eigenschaften wie timestamp, level und message besitzt.
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
    // Scrollt zum Ende des Containers, um die neuesten Logs anzuzeigen.
    logContainer.scrollTop = logContainer.scrollHeight;
}

/**
 * Sendet einen POST-Request an die angegebene URL und lädt bei Erfolg die Logs neu.
 * 
 * Bei erfolgreicher Durchführung des Requests wird fetchLogs aufgerufen, um die aktuellen Logs 
 * im UI anzuzeigen. Tritt ein Fehler auf, wird dieser in der Konsole protokolliert.
 *
 * @param {string} url - Die URL, an die der POST-Request gesendet wird.
 */
async function sendPostRequest(url) {
    try {
        const response = await fetch(url, { method: "POST" });
        if (!response.ok) {
            console.error("Fehler beim Senden der Anfrage:", response.statusText);
        } else {
            // Logs nach erfolgreicher Anfrage neu laden.
            fetchLogs();
        }
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

/* =====================================
         EVENT LISTENER INITIALISIERUNG
===================================== */

/**
 * Initialisiert die Event Listener, sobald der DOM-Inhalt geladen wurde.
 * 
 * Hier werden alle benötigten Event Listener registriert:
 * - Initiales Laden der Logs.
 * - Aktualisierung der Logs beim Wechsel des Log-Levels.
 * - Aktionen für Buttons wie Datenbank-Reset, Software-Update, Benutzerkommentar, Systemneustart, 
 *   Herunterfahren und Logout.
 */
document.addEventListener("DOMContentLoaded", () => {
    // Initiales Laden der Logs.
    fetchLogs();

    // Aktualisieren der Logs, wenn das Log-Level geändert wird.
    document.getElementById("log-level").addEventListener("change", fetchLogs);

    // Event Listener für den Datenbank-Reset-Button.
    document.getElementById("btnDatabaseReset").addEventListener("click", () => {
        modal.showDatabaseResetModal(fetchLogs);
    });

    // Event Listener für den Software-Update-Button.
    document.getElementById("btnUpdateSoftware").addEventListener("click", () => {
        modal.showUpdateModal(fetchLogs);
    });

    // Event Listener zum Hinzufügen eines Benutzerkommentars.
    document.getElementById("btnAddNote").addEventListener("click", () => {
        modal.showUserCommentModal(fetchLogs);
    });

    // Event Listener für den Reboot-Button.
    document.getElementById("btnReboot").addEventListener("click", () => {
        modal.showRebootModal(fetchLogs);
    });

    // Event Listener für den Shutdown-Button.
    document.getElementById("btnShutdown").addEventListener("click", () => {
        modal.showShutdownModal(fetchLogs);
    });

    // Event Listener für den Logout-Button: Führt Logout durch und navigiert zur Login-Seite.
    document.getElementById("logoutButton").addEventListener("click", async () => {
        await fetch("/logout", { method: "GET" });
        window.location.href = "/login";
    });
});
