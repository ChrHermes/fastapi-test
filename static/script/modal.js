import { fetchWithSpinner } from './spinner.js';

/* =====================================
   BASIS-MODAL-FUNKTION
   Diese Funktion bildet die Grundlage für alle spezifischen Modals,
   die im weiteren Verlauf verwendet werden.
===================================== */

/**
 * Zeigt ein generisches Modal an, das über ein Options-Objekt konfiguriert wird.
 * Die hier verwendeten DOM-Elemente werden einmalig zwischengespeichert, um wiederholte
 * Abfragen zu vermeiden.
 *
 * @param {Object} options - Konfigurationsobjekt für das Modal.
 */
export function showModal(options) {
    const {
        title = '',
        message = '',
        inputPlaceholder = '',
        passphrase, // Wenn gesetzt, wird der Info-Container angezeigt.
        safeButtonText = 'Abbrechen',
        dangerButtonText = 'Bestätigen',
        onConfirm = () => {},
        onCancel = () => {},
    } = options;

    // Abrufen der DOM-Elemente über eine Cache-Funktion.
    const { modal, overlay, modalTitle, messageElement, passphraseInfoContainer, passphraseText, inputField, dangerButton, safeButton } = getModalElements();

    // Inhalte setzen
    modalTitle.textContent = title;
    messageElement.innerHTML = message;

    // Passphrase-Info-Container nur anzeigen, wenn eine Passphrase gesetzt ist
    if (passphrase) {
        passphraseInfoContainer.style.display = "block";
        passphraseText.textContent = passphrase;
    } else {
        passphraseInfoContainer.style.display = "none";
    }

    // Inputfeld konfigurieren
    if (inputPlaceholder) {
        inputField.placeholder = inputPlaceholder;
    }
    inputField.value = "";
    inputField.focus();

    // Button-Texte anpassen
    dangerButton.textContent = dangerButtonText;
    safeButton.textContent = safeButtonText;

    // Modal und Overlay einblenden
    modal.classList.add("active");
    overlay.classList.add("active");

    // Handler für Bestätigung und Abbruch
    const confirmHandler = () => {
        if (passphrase && inputField.value.trim() !== passphrase) {
            alert("Falscher Bestätigungscode!");
            return;
        }
        onConfirm();
        cleanup();
    };

    const cancelHandler = () => {
        onCancel();
        cleanup();
    };

    // ESC-Taste zum Abbrechen abfangen
    const escHandler = (event) => {
        if (event.key === "Escape") {
            cancelHandler();
        }
    };

    // Aufräum-Funktion: Entfernt den ESC-Listener und blendet Modal und Overlay aus.
    const cleanup = () => {
        document.removeEventListener("keydown", escHandler);
        modal.classList.remove("active");
        overlay.classList.remove("active");
    };

    // Event-Listener registrieren – einmalige Ausführung garantiert durch { once: true }.
    dangerButton.addEventListener("click", confirmHandler, { once: true });
    safeButton.addEventListener("click", cancelHandler, { once: true });
    document.addEventListener("keydown", escHandler);
}

/**
 * Liefert die referenzierten DOM-Elemente und cached sie zur Vermeidung mehrfacher Abfragen.
 */
const modalElementsCache = {};
function getModalElements() {
    if (!modalElementsCache.modal) {
        modalElementsCache.modal = document.getElementById("confirmationModal");
        modalElementsCache.overlay = document.getElementById("modalOverlay");
        modalElementsCache.modalTitle = document.getElementById("modalTitle");
        modalElementsCache.messageElement = document.getElementById("modalMessage");
        modalElementsCache.passphraseInfoContainer = document.getElementById("passphraseInfoContainer");
        modalElementsCache.passphraseText = document.getElementById("passphraseText");
        modalElementsCache.inputField = document.getElementById("confirmationInput");
        modalElementsCache.dangerButton = document.getElementById("confirmAction");
        modalElementsCache.safeButton = document.getElementById("cancelAction");
    }
    return {
        modal: modalElementsCache.modal,
        overlay: modalElementsCache.overlay,
        modalTitle: modalElementsCache.modalTitle,
        messageElement: modalElementsCache.messageElement,
        passphraseInfoContainer: modalElementsCache.passphraseInfoContainer,
        passphraseText: modalElementsCache.passphraseText,
        inputField: modalElementsCache.inputField,
        dangerButton: modalElementsCache.dangerButton,
        safeButton: modalElementsCache.safeButton,
    };
}

/* =====================================
   SPEZIFISCHE MODAL-FUNKTIONEN
   Die folgenden Funktionen nutzen die Basisfunktion showModal,
   um kontextspezifische Modals anzuzeigen.
===================================== */

/**
 * Zeigt ein Modal zur Prüfung und Durchführung von Software-Updates an.
 * Nach erfolgreicher Ausführung kann ein Callback (z. B. zum Neuladen der Logs) aufgerufen werden.
 *
 * @param {Function} [onUpdateSuccess] - Optionaler Callback nach erfolgreichem Update.
 */
export async function showUpdateModal(onUpdateSuccess) {
    let message = "";
    try {
        // Abruf der Containerliste vom Backend
        const containersResponse = await fetch('/docker/containers/');
        if (!containersResponse.ok) {
            throw new Error("Fehler beim Abrufen der Container-Liste");
        }
        const containersList = await containersResponse.json();

        console.log(containersList) /* DEBUG */
        
        // Check der Softwareaktualisierungen
        const response = await fetch('/docker/check');
        if (!response.ok) {
            throw new Error("Fehler beim Prüfen der Softwareaktualisierungen");
        }
        const data = await response.json();

        message = `
        <table style="width:100%; border-collapse: collapse;">
          <thead>
            <tr>
                <th style="padding-bottom: 8px">Container</th>
                <th style="padding-bottom: 8px">Status</th>
            </tr>
          </thead>
          <tbody>`;
          
        /*const containers = ['backend', 'frontend', 'gateway', 'gcnia'];
        containers.forEach(container => {
            const info = data.updates[container];
            let status;
            if (info && info.available) {
                status = `<span style="color: green;">Neue Version ${info.newVersion}</span>`;
            } else {
                status = `<span style="color: red;">Kein Update verfügbar</span>`;
            }
            message += `
                <tr>
                    <td style="font-size: 0.9em;">${container}</td>
                    <td style="font-size: 0.9em;">${status}</td>
                </tr>`;
        });*/
        
        message += `
          </tbody>
        </table>`;
        
    } catch (error) {
        // Fehlermeldung in roter Schrift anzeigen
        message = `<p style="color: red; font-size: 0.9em;">${error.message}</p>`;
    }
    
    // Modal anzeigen – unabhängig vom Ergebnis des Checks
    showModal({
        title: "Software-Aktualisierungen prüfen",
        message: message,
        inputPlaceholder: "Bestätigungscode",
        passphrase: "gc-update",
        safeButtonText: "Abbrechen",
        dangerButtonText: "Aktualisierung durchführen",    
        onConfirm: async () => {
            alert("Aktualisierung gestartet - dieser Prozess kann einige Minuten dauern...");
            
            // Zuerst Images aktualisieren
            const updateResponse = await fetch('/docker/update', { method: 'POST' });
            if (!updateResponse.ok) {
                alert("Fehler beim Aktualisieren der Images.");
                return;
            }
            
            // Anschließend docker-compose Umgebung neu starten
            const restartResponse = await fetch('/docker/restart', { method: 'POST' });
            if (!restartResponse.ok) {
                alert("Fehler beim Neustarten der Umgebung.");
                return;
            }
            
            alert("Aktualisierung und Neustart wurden erfolgreich gestartet.");
            if (onUpdateSuccess) onUpdateSuccess();
        }
    });
}

/**
 * Zeigt ein Modal an, in dem der Benutzer einen Logeintrag eingeben kann.
 * Der eingegebene Text wird per POST-Request an "/log/custom" gesendet.
 * Bei erfolgreichem Speichern wird der Callback onLogAdded (falls übergeben) aufgerufen.
 *
 * @param {Function} onLogAdded - Callback, der nach dem Hinzufügen des Logeintrags ausgeführt wird.
 */
export function showUserCommentModal(onLogAdded) {
    showModal({
        title: "Benutzereintrag hinzufügen",
        message: "Bitte geben Sie Ihren Logeintrag ein:",
        inputPlaceholder: "Protokolleintrag",
        safeButtonText: "Abbrechen",
        dangerButtonText: "Eintrag hinzufügen",
        onConfirm: async () => {
            const note = document.getElementById("confirmationInput").value;
            try {
                const response = await fetch("/log/custom", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: note })
                });
                const data = await response.json();
                console.log("Logeintrag gespeichert:", data);
                if (typeof onLogAdded === "function") {
                    onLogAdded();
                }
            } catch (error) {
                console.error("Fehler beim Speichern des Logeintrags:", error);
            }
        },
        onCancel: () => console.log("Benutzereintrag abgebrochen")
    });
}

/**
 * Funktion zum Anzeigen des Datenbank-Reset-Modals.
 * Ruft zunächst die DB-Informationen ab und zeigt dann das Modal an.
 * Bei korrekter Bestätigung wird der Reset-Vorgang per API-Call gestartet.
 *
 * @param {Function} onResetSuccess - Optionaler Callback, der bei erfolgreichem Reset ausgeführt wird.
 */
export async function showDatabaseResetModal(onResetSuccess) {
    try {
        const response = await fetch("/database/info");
        if (!response.ok) {
            alert("Fehler beim Laden der DB-Informationen.");
            throw new Error("Fehler beim Laden der DB-Informationen.");
        }
        const data = await response.json();
        showModal({
            title: "Datenbank wirklich löschen?",
            message: `Sie sind dabei, die Datenbank zu löschen. Dies kann nicht rückgängig gemacht werden.<br><br>Größe der Datenbank: <span id="dbSize">${data.size}</span>`,
            inputPlaceholder: "Bestätigungscode",
            passphrase: "db-reset",
            safeButtonText: "Abbrechen",
            dangerButtonText: "Datenbank löschen",
            onConfirm: async () => {
                try {
                    const resetResponse = await fetchWithSpinner("/database/reset", { method: "POST" }, 30);
                    if (!resetResponse.ok) {
                        alert("Fehler beim Zurücksetzen der Datenbank.");
                    } else {
                        alert("Datenbank wurde zurückgesetzt.");
                        if (onResetSuccess) onResetSuccess();
                    }
                } catch (error) {
                    alert("Fehler: " + error.message);
                }
            }
        });
    } catch (error) {
        console.error("Fehler beim Abrufen der DB-Informationen:", error);
    }
}

/**
 * Zeigt ein Bestätigungsmodal zum Systemneustart an.
 * Es wird eine Passphrase abgefragt, um den Neustart durchzuführen.
 *
 * @param {Function} onSuccess - Optionaler Callback, z. B. zum Neuladen der Logs.
 */
export function showRebootModal(onSuccess) {
    showModal({
        title: "Systemneustart bestätigen",
        message: "Sie sind dabei, das System neu zu starten. Nicht gespeicherte Daten könnten verloren gehen.",
        inputPlaceholder: "Bestätigungscode",
        passphrase: "reboot-now",
        safeButtonText: "Abbrechen",
        dangerButtonText: "Jetzt neu starten",
        onConfirm: async () => {
            const response = await fetch("/system/reboot", { method: "POST" });
            if (!response.ok) {
                alert("Fehler beim Neustart des Systems.");
            } else {
                alert("System wird neu gestartet...");
                if (onSuccess) onSuccess();
            }
        }
    });
}

/**
 * Zeigt ein Bestätigungsmodal zum Herunterfahren des Systems an.
 * Auch hier muss eine definierte Passphrase eingegeben werden.
 *
 * @param {Function} onSuccess - Optionaler Callback, z. B. zum Neuladen der Logs.
 */
export function showShutdownModal(onSuccess) {
    showModal({
        title: "System herunterfahren?",
        message: "Sie sind dabei, das System herunterzufahren. Es wird anschließend nicht mehr erreichbar sein.",
        inputPlaceholder: "Bestätigungscode",
        passphrase: "shutdown-now",
        safeButtonText: "Abbrechen",
        dangerButtonText: "Jetzt herunterfahren",
        onConfirm: async () => {
            const response = await fetch("/system/shutdown", { method: "POST" });
            if (!response.ok) {
                alert("Fehler beim Herunterfahren des Systems.");
            } else {
                alert("System wird heruntergefahren...");
                if (onSuccess) onSuccess();
            }
        }
    });
}
