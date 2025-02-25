// modal.js
export function showModal(options) {
    const {
        title = '',
        message = '',
        inputPlaceholder = '',
        passphrase = '',
        onConfirm = () => {}
    } = options;

    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const modalTitle = document.getElementById("modalTitle");
    const messageElement = document.getElementById("modalMessage");
    const inputField = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");

    // Inhalte setzen
    modalTitle.textContent = title;
    messageElement.innerHTML = message;
    inputField.placeholder = inputPlaceholder;
    inputField.value = "";
    inputField.focus();

    // Modal und Overlay anzeigen
    modal.classList.add("active");
    overlay.classList.add("active");

    const confirmHandler = () => {
        if (!passphrase || inputField.value === passphrase) {
            onConfirm();
            cleanup();
        } else {
            alert("Falscher Bestätigungscode!");
        }
    };

    function cleanup() {
        confirmButton.removeEventListener("click", confirmHandler);
        modal.classList.remove("active");
        overlay.classList.remove("active");
    }

    confirmButton.addEventListener("click", confirmHandler);
    cancelButton.addEventListener("click", cleanup, { once: true });
}
