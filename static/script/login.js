/* ---------------------------------------------- EVENT LISTENER */
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!username || !password) {
            document.getElementById("error-message").innerText = "Benutzername und Passwort erforderlich!";
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username, password })
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const data = await response.json();
                document.getElementById("error-message").innerText = data.detail;
            }
        } catch (error) {
            console.error("Fehler beim Login:", error);
            document.getElementById("error-message").innerText = "Serverfehler. Bitte später versuchen.";
        }
    });
});