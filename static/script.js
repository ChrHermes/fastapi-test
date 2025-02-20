/* ---------------------------------------------- EVENT LISTENER */
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("confirmationModal");
    const overlay = document.getElementById("modalOverlay");
    const overlayInput = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmAction");
    const cancelButton = document.getElementById("cancelAction");
    const actionButton = document.querySelector(".btnGC"); // Button mit Klasse btnGC

    function showConfirmationModal() {
        modal.classList.add("active");
        overlay.classList.add("active");
        overlayInput.value = "";
    }

    actionButton.addEventListener("click", showConfirmationModal);

    cancelButton.addEventListener("click", function () {
        modal.classList.remove("active");
        overlay.classList.remove("active");
    });

    confirmButton.addEventListener("click", function () {
        const inputValue = document.getElementById("confirmationInput").value;
        if (inputValue === "db-reset") {
            modal.classList.remove("active");
            overlay.classList.remove("active");
            document.getElementById("log").innerHTML += formatLogMessage("Datenbank zurückgesetzt!");
            document.getElementById("log").scrollTop = document.getElementById("log").scrollHeight;
            // Hier später API-Call einfügen
        } else {
            alert("Falscher Bestätigungscode!");
        }
    });
});

/* ---------------------------------------------- LOGIN */
async function sendRequest(endpoint) {
    const response = await fetch(endpoint, {
        method: "POST",
        headers: { 'Authorization': 'Basic ' + btoa('admin:password') }
    });
    const data = await response.json();
    document.getElementById("log").innerHTML += formatLogMessage(data.message);
    document.getElementById("log").scrollTop = document.getElementById("log").scrollHeight;
}

/* ---------------------------------------------- THEME */
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeButtonText(isDark);
}

function updateThemeButtonText(isDark) {
    const button = document.getElementById('theme-toggle');
    button.textContent = isDark ? '🌞' : '🌚';
}

/* ---------------------------------------------- MODAL */
function showConfirmationModal() {
    const modal = document.getElementById('confirmation-modal');
    modal.style.display = 'block';
}

function hideConfirmationModal() {
    const modal = document.getElementById('confirmation-modal');
    modal.style.display = 'none';
}

function confirmAction() {
    const input = document.getElementById('confirmation-input').value;
    if (input === 'db-reset') {
        alert('Datenbank wird zurückgesetzt...');
        hideConfirmationModal();
        // Hier kann später der API-Call eingefügt werden
    } else {
        alert('Falscher Bestätigungscode!');
    }
}

/* ---------------------------------------------- LOGGING */
function formatLogMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    return `<div class='log-entry'><span class='timestamp'>[${timestamp}]</span> ${message}</div>`;
}