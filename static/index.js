/* =====================================
   GLOBALE FUNKTIONEN FÜR LOGGING & UI
===================================== */

/**
 * Holt die Logs vom Backend und zeigt sie an.
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
 * Zeigt die Logs im gewünschten Format im Container an und scrollt automatisch nach unten.
 * Format: "dd.mm.yyyy HH:MM:SS [LEVEL] Message"
 * @param {Array} logs - Array von Log-Einträgen.
 */
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
    
    // Automatisches Scrollen nach unten, sodass das aktuellste Log sichtbar ist.
    logContainer.scrollTop = logContainer.scrollHeight;
}

/**
 * Lädt die Logs.
 */
function loadLogs() {
    fetchLogs();
}

/**
 * Sendet eine POST-Anfrage an die angegebene URL und lädt danach die Logs neu.
 * @param {string} url - Die URL, an die die Anfrage gesendet wird.
 */
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
           MODAL-FUNKTIONALITÄT
===================================== */

/**
 * Zeigt das Modal mit dynamischem Text und Passphrase an.
 * @param {string} message - Nachricht, die im Modal angezeigt wird. (HTML ist erlaubt)
 * @param {string} passphrase - Erforderliche Eingabe zur Bestätigung.
 * @param {Function} onConfirm - Callback, der bei richtiger Eingabe ausgeführt wird.
 */
function showModal(message, passphrase, onConfirm) {
    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const messageElement = document.getElementById("modalMessage");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");

    // Setzt den dynamischen Nachrichtentext (HTML wird unterstützt)
    messageElement.innerHTML = message;
    inputField.value = "";
    inputField.focus();

    // Zeigt Modal und Overlay an
    modal.classList.add("active");
    overlay.classList.add("active");

    const confirmHandler = async () => {
        if (inputField.value === passphrase) {
            onConfirm();
            cleanup();
        } else {
            alert("Falscher Bestätigungscode!");
        }
    };

    const cleanup = () => {
        confirmButton.removeEventListener("click", confirmHandler);
        modal.classList.remove("active");
        overlay.classList.remove("active");
    };

    confirmButton.addEventListener("click", confirmHandler);
    cancelButton.addEventListener("click", cleanup, { once: true });
}

// Beispiel: Funktion, die DB-Info lädt und Modal öffnet
async function openDbDeleteModal() {
    try {
        const response = await fetch("/db-info");
        if (!response.ok) {
            console.error("Fehler beim Laden der DB-Info");
            return;
        }
        const data = await response.json();
        const dbSize = data.size || "unbekannt";

        // Füge die Größe in den Text ein
        // Du kannst hier natürlich auch dein "showModal(...)" nutzen,
        // wenn du den Text dynamisch anpassen möchtest.
        document.getElementById("dbSize").textContent = dbSize;

        // Modal anzeigen (z. B. showModal-Funktion aus index.js)
        showModal(
            `Sie sind dabei, die Datenbank mit Größe ${dbSize} zu löschen.<br>Dies kann nicht rückgängig gemacht werden.`,
            "db-reset",
            () => {
                sendRequest("/log/btnGC");
            }
        );
    } catch (error) {
        console.error("Fehler:", error);
    }
}


/* =====================================
       CONTAINER-GRÖSSEN-ANPASSUNG
===================================== */

/**
 * Aktualisiert die Container-Breite und passt die CSS-Variable "--container-width" an.
 */
function updateContainerWidth() {
    const container = document.querySelector(".container");
    if (container) {
        const width = container.clientWidth + "px";
        container.style.setProperty("--container-width", width);
    }
}

// Beim Laden der Seite: Container-Größe initialisieren
window.addEventListener("load", () => {
    const logContainer = document.querySelector(".log-container");
    if (logContainer) {
        logContainer.style.width = logContainer.clientWidth + "px";
        logContainer.style.height = logContainer.clientHeight + "px";
    }
    updateContainerWidth();
});

// Beim Ändern der Fenstergröße: Container-Größe anpassen
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

    // Button GC: Öffnet das Modal für den Datenbank-Reset mit dynamischem Text und Passphrase
    document.getElementById("btnGC").addEventListener("click", function () {
        showModal(
            "Bitte geben Sie <span class='code-highlight'>db-reset</span> ein, um die Datenbank zurückzusetzen.",
            "db-reset",
            () => {
                sendRequest("/log/btnGC");
            }
        );
    });

    // Button 2: Direkte Anfrage senden
    document.getElementById("btn2").addEventListener("click", function () {
        sendRequest("/log/button2");
    });

    // Button 3: Direkte Anfrage senden (Backend-Endpunkt muss existieren)
    document.getElementById("btn3").addEventListener("click", function () {
        sendRequest("/log/button3");
    });

    // Button 4: Direkte Anfrage senden
    document.getElementById("btn4").addEventListener("click", function () {
        sendRequest("/log/button4");
    });
});

/* =====================================
                LOGOUT
===================================== */

// Logout-Button: Leitet zum Logout um
document.getElementById("logoutButton").addEventListener("click", async function() {
    await fetch("/logout", { method: "GET" });
    window.location.href = "/login";
});
