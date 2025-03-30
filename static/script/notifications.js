/**
 * Liefert das Material Icon Element für einen gegebenen Benachrichtigungstyp.
 * Dabei wird die Icon-Größe aus der CSS-Variable --toast-icon-size (Fallback: 20px) entnommen.
 *
 * @param {string} type - Der Typ der Benachrichtigung ("success", "info", "warning", "error").
 * @returns {HTMLElement} - Das Icon-Element.
 */
function getIconElementForType(type) {
    const icon = document.createElement("span");
    icon.classList.add("material-icons");
    // Hole die Icon-Größe aus den CSS-Variablen, Fallback: 20px.
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
            icon.textContent = "error";
            break;
        default:
            icon.textContent = "";
    }
    return icon;
}

/**
 * Ermittelt die Hintergrundfarbe für einen Benachrichtigungstyp anhand von CSS-Variablen.
 *
 * @param {string} type - Der Typ der Benachrichtigung ("success", "info", "warning", "error").
 * @returns {string} - Die Hintergrundfarbe.
 */
function getBackgroundColorForType(type) {
    const rootStyles = getComputedStyle(document.documentElement);
    let bg;
    switch (type) {
        case "success":
            bg = rootStyles.getPropertyValue('--toast-success-bg').trim() || "#4caf50";
            break;
        case "info":
            bg = rootStyles.getPropertyValue('--toast-info-bg').trim() || "#2196f3";
            break;
        case "warning":
            bg = rootStyles.getPropertyValue('--toast-warning-bg').trim() || "#ff9800";
            break;
        case "error":
            bg = rootStyles.getPropertyValue('--toast-error-bg').trim() || "#f44336";
            break;
        default:
            bg = "#333";
    }
    return bg;
}

/**
 * Zeigt eine Toast-Benachrichtigung an.
 *
 * @param {string} type - Der Typ der Benachrichtigung: "success", "info", "warning" oder "error".
 * @param {string} message - Die anzuzeigende Nachricht.
 * @param {number} [duration=3000] - Dauer in Millisekunden, wie lange die Benachrichtigung sichtbar bleibt.
 */
export function showToast(type, message, duration = 3000) {
    // Container für Toasts erstellen, falls noch nicht vorhanden.
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.style.position = "fixed";
        container.style.top = "20px";
        container.style.right = "20px";
        container.style.zIndex = "9999";
        container.style.display = "flex";
        container.style.flexDirection = "column";
        container.style.gap = "10px";
        document.body.appendChild(container);
    }
    
    // Toast-Element erstellen und stylen.
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.padding = "10px 20px";
    toast.style.borderRadius = "4px";
    toast.style.color = "#fff";
    // Hintergrundfarbe aus CSS-Variablen oder Fallback.
    toast.style.backgroundColor = getBackgroundColorForType(type);
    // Schriftgröße aus CSS-Variable --toast-font-size (Fallback: 14px).
    const rootStyles = getComputedStyle(document.documentElement);
    toast.style.fontSize = rootStyles.getPropertyValue('--toast-font-size').trim() || "14px";
    toast.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
    toast.style.opacity = "0";
    toast.style.transition = "opacity 0.5s ease";
    
    // Icon-Element einfügen.
    const iconElement = getIconElementForType(type);
    iconElement.style.marginRight = "8px";
    toast.appendChild(iconElement);
    
    // Nachrichtentext hinzufügen.
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
