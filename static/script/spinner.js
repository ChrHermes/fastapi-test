/**
 * spinner.js
 *
 * Dieses Modul stellt Funktionen zur Verfügung, um einen Lade-Spinner
 * mitsamt Overlay anzuzeigen und Fetch-Aufrufe mit einem Timeout zu versehen.
 *
 * Funktionen:
 *   - showSpinner(): Blendet das Overlay mit dem Spinner ein.
 *   - hideSpinner(): Blendet das Overlay mit dem Spinner aus.
 *   - fetchWithSpinner(url, options, timeoutDuration):
 *       Führt einen Fetch-Aufruf aus, zeigt währenddessen den Spinner an und
 *       löst nach Ablauf der Timeout-Dauer (Standard: 30 Sekunden) einen Fehler aus,
 *       falls keine Antwort erfolgt.
 */

export function showSpinner() {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) {
    overlay.style.display = "flex"; // "flex" sorgt dafür, dass der Spinner zentriert angezeigt wird
  }
}

export function hideSpinner() {
  const overlay = document.getElementById("loadingOverlay");
  if (overlay) {
    overlay.style.display = "none";
  }
}

/**
 * Führt einen Fetch-Aufruf aus und zeigt dabei einen Lade-Spinner an.
 * Falls die Antwort länger als die angegebene Timeout-Dauer (in Sekunden) dauert,
 * wird ein Fehler ausgelöst.
 *
 * @param {string} url - Die URL für den Fetch-Aufruf.
 * @param {object} options - Optionen, die an fetch übergeben werden.
 * @param {number} [timeoutSeconds=30] - Timeout-Dauer in Sekunden (Standard: 30 Sekunden).
 * @returns {Promise<Response>} Ein Promise, das die Antwort des Fetch-Aufrufs zurückgibt.
 */
export function fetchWithSpinner(url, options, timeoutSeconds = 30) {
    showSpinner();
  
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        hideSpinner();
        reject(new Error("Timeout überschritten"));
      }, timeoutSeconds * 1000);
  
      fetch(url, options)
        .then(response => {
          clearTimeout(timeout);
          hideSpinner();
          resolve(response);
        })
        .catch(err => {
          clearTimeout(timeout);
          hideSpinner();
          reject(err);
        });
    });
}
