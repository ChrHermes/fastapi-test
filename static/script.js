// ---------------------------------------------- LOGIN
async function sendRequest(endpoint) {
    const response = await fetch(endpoint, {
        method: "POST",
        headers: { 'Authorization': 'Basic ' + btoa('admin:password') }
    });
    const data = await response.json();
    document.getElementById("log").innerHTML += formatLogMessage(data.message);
    document.getElementById("log").scrollTop = document.getElementById("log").scrollHeight;
}

// ---------------------------------------------- THEME
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

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = savedTheme ? savedTheme === 'dark' : systemPrefersDark;
    document.body.classList.toggle('dark-mode', isDark);
    updateThemeButtonText(isDark);
});

// ---------------------------------------------- MODAL
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

// ---------------------------------------------- LOGGING
function formatLogMessage(message) {
    const timestamp = new Date().toLocaleTimeString();
    return `<div class='log-entry'><span class='timestamp'>[${timestamp}]</span> ${message}</div>`;
}