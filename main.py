from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging

app = FastAPI()
security = HTTPBasic()

# Logger einrichten
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Einfache Benutzerauthentifizierung
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "admin" and credentials.password == "password":
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Basic"},
    )

# API-Endpunkte
@app.post("/log/button1")
def log_button1(user: str = Depends(get_current_user)):
    logger.info("Button 1 wurde geklickt")
    return {"message": "Button 1 ausgelöst"}

@app.post("/log/button2")
def log_button2(user: str = Depends(get_current_user)):
    logger.info("Button 2 wurde geklickt")
    return {"message": "Button 2 ausgelöst"}

# HTML-Seite für das Frontend
html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FastAPI Web Interface</title>
    <script>
        async function sendRequest(endpoint) {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { 'Authorization': 'Basic ' + btoa('admin:password') }
            });
            const data = await response.json();
            document.getElementById("log").textContent += data.message + "\n";
        }
    </script>
</head>
<body>
    <h1>FastAPI Web Interface</h1>
    <button onclick="sendRequest('/log/button1')">Button 1</button>
    <button onclick="sendRequest('/log/button2')">Button 2</button>
    <pre id="log" style="border:1px solid black; padding:10px; height:200px; overflow:auto;"></pre>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_page(user: str = Depends(get_current_user)):
    return html_content

