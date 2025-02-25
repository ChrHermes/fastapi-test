/* ---------------------------------------------- EVENT LISTENER */
document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.textContent = "🌞";
    } else {
        themeToggle.textContent = "🌚";
    }

    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        themeToggle.textContent = isDark ? "🌞" : "🌚";
    });
});

/* ---------------------------------------------- LOGIN */
async function sendRequest(endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { 'Authorization': 'Basic ' + btoa('admin:password') }
        });
        const data = await response.json();
        appendLog(data.message);
    } catch (error) {
        console.error("Fehler beim Senden der Anfrage:", error);
    }
}

// Automatische Umleitung zur Login-Seite, falls nicht eingeloggt
(async function checkLogin() {
    try {
        const response = await fetch("/protected");
        if (!response.ok) {
            window.location.href = "/login";
        }
    } catch (error) {
        console.error("Fehler bei der Login-Prüfung:", error);
        window.location.href = "/login";
    }
})();