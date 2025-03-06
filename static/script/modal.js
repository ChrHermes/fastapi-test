// modal.js
export function showModal(options) {
    const {
        title = '',
        message = '',
        inputPlaceholder = '',
        passphrase, // optional; falls gesetzt, wird der Passphrase-Bereich angezeigt
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
    
    if (passphrase || inputPlaceholder) {
        passphraseContainer.style.display = "block";
        if (passphrase) {
            passphraseText.textContent = passphrase;
        } else {
            passphraseText.textContent = "";
        }
        inputField.placeholder = inputPlaceholder;
        inputField.value = "";
        inputField.focus();
    } else {
        passphraseContainer.style.display = "none";
    }

    // Button-Texte anpassen
    dangerButton.textContent = dangerButtonText;
    safeButton.textContent = safeButtonText;

    // Modal und Overlay anzeigen
    modal.classList.add("active");
    overlay.classList.add("active");

    // Bestätigungs-Handler
    const confirmHandler = () => {
        // Falls eine Passphrase definiert wurde, prüfen wir die Eingabe
        if (passphrase && inputField.value !== passphrase) {
            alert("Falscher Bestätigungscode!");
            return;
        }
        onConfirm();
        cleanup();
    };

    // Abbruch-Handler (auch für ESC-Taste)
    const cancelHandler = () => {
        onCancel();
        cleanup();
    };

    // ESC-Taste abfangen
    function escHandler(event) {
        if (event.key === "Escape") {
            cancelHandler();
        }
    }

    // Aufräumen: entfernt Event-Listener und blendet Modal/Overlay aus
    function cleanup() {
        dangerButton.removeEventListener("click", confirmHandler);
        safeButton.removeEventListener("click", cancelHandler);
        document.removeEventListener("keydown", escHandler);
        modal.classList.remove("active");
        overlay.classList.remove("active");
    }

    // Event-Listener registrieren
    dangerButton.addEventListener("click", confirmHandler);
    safeButton.addEventListener("click", cancelHandler, { once: true });
    document.addEventListener("keydown", escHandler);
}
