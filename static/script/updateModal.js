// updateModal.js
import { showModal } from './modal.js';

export async function checkAndShowUpdateModal() {
    try {
        // API-Call zum Prüfen der Softwareaktualisierungen
        const response = await fetch('/registry/check');
        if (!response.ok) {
            throw new Error("Fehler beim Prüfen der Softwareaktualisierungen");
        }
        const data = await response.json();

        // Beispiel: data.updates enthält Informationen für jeden Container
        // Wir bauen eine Nachricht, die den Update-Status darstellt
        let message = 'Verfügbare Updates:<br>';
        const containers = ['backend', 'frontend', 'gateway', 'gcnia'];
        containers.forEach(container => {
            const info = data.updates[container];
            if (info && info.available) {
                message += `<strong>${container}</strong>: Neue Version ${info.newVersion}<br>`;
            } else {
                message += `<strong>${container}</strong>: Kein Update verfügbar<br>`;
            }
        });

        // Modal anzeigen – hier wird der Nutzer gebeten, die Aktualisierung zu bestätigen
        showModal({
            title: "Software-Aktualisierungen prüfen",
            message: message,
            inputPlaceholder: "Passphrase eingeben",
            passphrase: "update-confirm",  // Passe die Passphrase nach Bedarf an
            onConfirm: async () => {
                // API-Call zum Starten der Aktualisierung
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
