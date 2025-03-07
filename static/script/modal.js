// modal.js

/**
 * Generisches Modal, das via Options-Objekt konfiguriert wird.
 */
export function showModal(options) {
    const {
        title = '',
        message = '',
        inputPlaceholder = '',
        passphrase, // optional; zeigt den Passphrase-Bereich an, wenn gesetzt
        safeButtonText = 'Abbrechen', // Text für den sicheren Abbruch-Button
        dangerButtonText = 'Bestätigen', // Text für den gefährlichen Bestätigungs-Button
        onConfirm = () => {},
        onCancel = () => {},
    } = options;

    // Referenzen zu den DOM-Elementen des Modals
    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const modalTitle = document.getElementById("modalTitle");
    const messageElement = document.getElementById("modalMessage");
    const passphraseContainer = document.getElementById("passphraseContainer");
    const passphraseText = document.getElementById("passphraseText");
    const inputField = document.getElementById("confirmationInput");
    const dangerButton = document.getElementById("confirmAction");
    const safeButton = document.getElementById("cancelAction");

    // Inhalte setzen
    modalTitle.textContent = title;
    messageElement.innerHTML = message;

    // Input anzeigen, wenn entweder passphrase oder inputPlaceholder gesetzt ist
    if (passphrase || inputPlaceholder) {
        passphraseContainer.style.display = "block";
        passphraseText.textContent = passphrase ? passphrase : "";
        inputField.placeholder = inputPlaceholder;
        inputField.value = "";
        inputField.focus();
    } else {
        passphraseContainer.style.display = "none";
    }

    // Button-Texte anpassen
    dangerButton.textContent = dangerButtonText;
    safeButton.textContent = safeButtonText;

    // Modal und Overlay einblenden
    modal.classList.add("active");
    overlay.classList.add("active");

    // Handler für Bestätigung und Abbruch
    const confirmHandler = () => {
        if (passphrase && inputField.value !== passphrase) {
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

    // Aufräum-Funktion: Entfernt Event-Listener und blendet Modal/Overlay aus
    const cleanup = () => {
        dangerButton.removeEventListener("click", confirmHandler);
        safeButton.removeEventListener("click", cancelHandler);
        document.removeEventListener("keydown", escHandler);
        modal.classList.remove("active");
        overlay.classList.remove("active");
    };

    // Event-Listener registrieren
    dangerButton.addEventListener("click", confirmHandler);
    safeButton.addEventListener("click", cancelHandler, { once: true });
    document.addEventListener("keydown", escHandler);
}

/**
 * Zeigt das Software-Update-Modal an, welches Update-Informationen per API-Call abruft.
 */
export async function showUpdateModal() {
    try {
        const response = await fetch('/registry/check');
        if (!response.ok) throw new Error("Fehler beim Prüfen der Softwareaktualisierungen");
        const data = await response.json();

        // Update-Informationen zusammenfassen
        let message = `
        <table style="width:100%; border-collapse: collapse;">
          <thead>
            <tr>
                <th style="padding-bottom: 8px">Container</th>
                <th style="padding-bottom: 8px">Status</th>
            </tr>
          </thead>
          <tbody>`;
        const containers = ['backend', 'frontend', 'gateway', 'gcnia'];
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
            });
        message += `
            </tbody>
            </table>`;

        // Modal anzeigen und Passphrase abfragen
        showModal({
            title: "Software-Aktualisierungen prüfen",
            message: message,
            inputPlaceholder: "Passphrase eingeben",
            passphrase: "gc-update",
            safeButtonText: "Abbrechen",
            dangerButtonText: "Aktualisierung durchführen",    
            onConfirm: async () => {
                const updateResponse = await fetch('/registry/update', { method: 'POST' });
                if (!updateResponse.ok) {
                    alert("Fehler beim Starten der Aktualisierung.");
                } else {
                    alert("Aktualisierung wurde gestartet.");
                }
            }
        });
    } catch (error) {
        console.error("Fehler:", error);
    }
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
        inputPlaceholder: "Dein Logeintrag hier...",
        safeButtonText: "Abbrechen",
        dangerButtonText: "Eintrag hinzufügen",
        onConfirm: () => {
            const note = document.getElementById("confirmationInput").value;
            fetch("/log/custom", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: note })
            })
            .then(response => response.json())
            .then(data => {
                console.log("Logeintrag gespeichert:", data);
                if (typeof onLogAdded === "function") {
                    onLogAdded();
                }
            })
            .catch(error => console.error("Fehler beim Speichern des Logeintrags:", error));
        },
        onCancel: () => console.log("Benutzereintrag abgebrochen")
    });
}

/**
 * Funktion zum Anzeigen des Datenbank-Reset-Modals.
 * Ruft zunächst die DB-Informationen ab und zeigt dann das Modal an.
 * Bei korrekter Bestätigung wird der Reset-Vorgang per API-Call gestartet.
 *
 * @param {function} onResetSuccess - Optionaler Callback, der bei erfolgreichem Reset aufgerufen wird (z. B. zum Neuladen der Logs).
 */
export async function showDatabaseResetModal(onResetSuccess) {
    try {
        const response = await fetch("/database/info");
        if (!response.ok) throw new Error("Fehler beim Laden der DB-Informationen.");
        const data = await response.json();
        // Die DB-Größe wird direkt in der Nachricht eingebaut
        showModal({
            title: "Datenbank wirklich löschen?",
            message: `Sie sind dabei, die Datenbank zu löschen. Dies kann nicht rückgängig gemacht werden.<br><br>Größe der Datenbank: <span id="dbSize">${data.size}</span>`,
            inputPlaceholder: "Bestätigungscode",
            passphrase: "db-reset",
            safeButtonText: "Abbrechen",
            dangerButtonText: "Datenbank löschen",    
            onConfirm: async () => {
                const resetResponse = await fetch("/database/reset", { method: "POST" });
                if (!resetResponse.ok) {
                    alert("Fehler beim Zurücksetzen der Datenbank.");
                } else {
                    alert("Datenbank wurde zurückgesetzt.");
                    if (onResetSuccess) onResetSuccess();
                }
            }
        });
    } catch (error) {
        console.error("Fehler beim Abrufen der DB-Informationen:", error);
    }
}