/* index.js */

// Importiere die Modal-Funktion aus modal.js
import { showModal } from './modal.js';
import { checkAndShowUpdateModal } from './updateModal.js';

/* =====================================
   GLOBALE FUNKTIONEN FÜR LOGGING & UI
===================================== */

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
            const logEntry = document.createElement("div");
            logEntry.textContent = `${log.timestamp} [${log.level}] ${log.message}`;
            logContainer.appendChild(logEntry);
        }
    });
    
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
            fetchLogs();
        }
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

/* =====================================
       CONTAINER-GRÖSSEN-ANPASSUNG
===================================== */

function updateContainerWidth() {
    const container = document.querySelector(".container");
    if (container) {
        const width = container.clientWidth + "px";
        container.style.setProperty("--container-width", width);
    }
}

window.addEventListener("load", () => {
    const logContainer = document.querySelector(".log-container");
    if (logContainer) {
        logContainer.style.width = logContainer.clientWidth + "px";
        logContainer.style.height = logContainer.clientHeight + "px";
    }
    updateContainerWidth();
});

window.addEventListener("resize", updateContainerWidth);

/* =====================================
         EVENT LISTENER INITIALISIERUNG
===================================== */

document.addEventListener("DOMContentLoaded", function () {
    // Logs laden
    loadLogs();

    // Bei Änderung des Log-Levels: Neue Logs laden
    const logLevelSelect = document.getElementById("log-level");
    logLevelSelect.addEventListener("change", fetchLogs);

    // Button GC: Modal für den Datenbank-Reset öffnen
    document.getElementById("buttonDatabaseReset").addEventListener("click", async () => {
        try {
            // DB-Informationen vom Backend abrufen
            const response = await fetch("/database/info");
            if (!response.ok) {
                throw new Error("Fehler beim Laden der DB-Informationen.");
            }
            const data = await response.json();
            
            // Modal öffnen
            showModal({
                title: "Datenbank wirklich löschen?",
                message: "Sie sind dabei, die Datenbank zu löschen. Dies kann nicht rückgängig gemacht werden.<br><br>Größe der Datenbank: <span id=\"dbSize\"></span>",
                inputPlaceholder: "Bestätigungscode",
                passphrase: "db-reset",
                onConfirm: () => {
                    sendRequest("/database/reset");
                }
            });
            
            // Nach dem Öffnen des Modals die DB-Größe in das span einsetzen
            document.getElementById("dbSize").textContent = data.size;
        } catch (error) {
            console.error("Fehler beim Abrufen der DB-Informationen:", error);
        }
    });

    document.getElementById("btnUpdateSoftware").addEventListener("click", () => {
        checkAndShowUpdateModal();
    });

    // // Button 2: Direkte Anfrage senden
    // document.getElementById("btn2").addEventListener("click", function () {
    //     sendRequest("/log/button2");
    // });

    // Button 3: Direkte Anfrage senden
    document.getElementById("btn3").addEventListener("click", function () {
        sendRequest("/log/button3");
    });

    // Button 4: Direkte Anfrage senden
    document.getElementById("btn4").addEventListener("click", function () {
        sendRequest("/log/button4");
    });

    // Logout-Button: Logout durchführen und zur Login-Seite navigieren
    document.getElementById("logoutButton").addEventListener("click", async function() {
        await fetch("/logout", { method: "GET" });
        window.location.href = "/login";
    });
});
