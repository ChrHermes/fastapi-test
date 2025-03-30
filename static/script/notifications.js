/**
 * Liefert das Material Icon Element für einen gegebenen Benachrichtigungstyp.
 * Hier nutzen wir Google Fonts Icons. Stelle sicher, dass du im HTML folgenden Link eingebunden hast:
 * <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
 *
 * @param {string} type - "success", "info", "warning" oder "error".
 * @returns {HTMLElement} - Das Icon-Element.
 */
function getIconElementForType(type) {
    const icon = document.createElement("span");
    icon.classList.add("material-icons");
    icon.style.marginRight = "8px";
    // Hole die Icon-Größe aus der CSS-Variable
    const rootStyles = getComputedStyle(document.documentElement);
    const iconSize = rootStyles.getPropertyValue('--toast-icon-size').trim() || '20px';
    icon.style.fontSize = iconSize;
    switch (type) {
        case "success":
            icon.textContent = "check_circle";
            break;
        case "info":
            icon.textContent = "info";
            break;
        case "warning":
            icon.textContent = "warning";
            break;
        case "error":
            icon.textContent = "report";
            break;
        default:
            icon.textContent = "info";
    }
    return icon;
}

/**
 * Ermittelt die Hintergrundfarbe für einen Benachrichtigungstyp anhand der in base.css definierten Variablen.
 *
 * @param {string} type - "success", "info", "warning" oder "error".
 * @returns {string} - Die Hintergrundfarbe.
 */
function getBackgroundColorForType(type) {
    const rootStyles = getComputedStyle(document.documentElement);
    let bg;
    switch (type) {
        case "success":
            bg = rootStyles.getPropertyValue('--toast-success-bg').trim();
            break;
        case "info":
            bg = rootStyles.getPropertyValue('--toast-info-bg').trim();
            break;
        case "warning":
            bg = rootStyles.getPropertyValue('--toast-warning-bg').trim();
            break;
        case "error":
            bg = rootStyles.getPropertyValue('--toast-error-bg').trim();
            break;
        default:
            bg = "#333";
    }
    return bg;
}

/**
 * Ermittelt den Textfarbe-Wert für einen Benachrichtigungstyp anhand der in base.css definierten Variablen.
 *
 * @param {string} type - "success", "info", "warning" oder "error".
 * @returns {string} - Die Textfarbe.
 */
function getTextColorForType(type) {
    const rootStyles = getComputedStyle(document.documentElement);
    let color;
    switch (type) {
        case "success":
            color = rootStyles.getPropertyValue('--toast-success-text').trim();
            break;
        case "info":
            color = rootStyles.getPropertyValue('--toast-info-text').trim();
            break;
        case "warning":
            color = rootStyles.getPropertyValue('--toast-warning-text').trim();
            break;
        case "error":
            color = rootStyles.getPropertyValue('--toast-error-text').trim();
            break;
        default:
            color = "#fff";
    }
    return color;
}

/**
 * Zeigt eine Toast-Benachrichtigung an.
 *
 * @param {string} type - "success", "info", "warning" oder "error".
 * @param {string} message - Die anzuzeigende Nachricht.
 * @param {number} [duration=5000] - Dauer in Millisekunden, wie lange der Toast sichtbar bleibt.
 */
export function showToast(type, message, duration = 5000) {
    // Container für Toasts erstellen, falls noch nicht vorhanden.
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }
    
    // Toast-Element erstellen
    const toast = document.createElement("div");
    toast.classList.add("toast", `toast-${type}`);
    
    // Setze Schriftgröße (aus CSS-Variablen) falls gewünscht:
    const rootStyles = getComputedStyle(document.documentElement);
    toast.style.fontSize = rootStyles.getPropertyValue('--toast-font-size').trim() || "14px";
    
    // Anstatt die Hintergrundfarbe und Textfarbe im JS zu setzen, 
    // erfolgt das Styling über die CSS-Klassen in der base.css.
    // Falls du sie trotzdem im JS setzen möchtest:
    // toast.style.backgroundColor = getBackgroundColorForType(type);
    // toast.style.color = getTextColorForType(type);
    
    // Icon hinzufügen
    const iconElement = getIconElementForType(type);
    toast.appendChild(iconElement);
    
    // Nachricht hinzufügen
    const messageSpan = document.createElement("span");
    messageSpan.textContent = message;
    toast.appendChild(messageSpan);
    
    container.appendChild(toast);
    // Erzwinge Reflow, damit der Übergang wirkt.
    window.getComputedStyle(toast).opacity;
    toast.style.opacity = "1";
    
    // Toast nach Ablauf der Dauer ausblenden und entfernen.
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => {
            if (toast.parentNode === container) {
                container.removeChild(toast);
            }
        }, 500);
    }, duration);
}
