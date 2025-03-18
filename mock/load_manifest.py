import os
import sys
import re
import json
import requests
from dotenv import load_dotenv

# Globales Dictionary zur Sammlung der übertragenen Bytes (gesendet + empfangen)
transfer_summary = {}

def record_transfer(label, bytes_amount):
    """Fügt für das gegebene Label die Anzahl der übertragenen Bytes zur globalen Summe hinzu."""
    if label in transfer_summary:
        transfer_summary[label] += bytes_amount
    else:
        transfer_summary[label] = bytes_amount

def measure_prepared_request(prepared):
    """
    Berechnet die ungefähre Größe der zu sendenden Daten aus einem PreparedRequest.
    Dabei werden die Request-Line, die Header und der Body (falls vorhanden) berücksichtigt.
    """
    request_line = f"{prepared.method} {prepared.url} HTTP/1.1\r\n"
    headers_str = "".join(f"{k}: {v}\r\n" for k, v in prepared.headers.items())
    body = prepared.body if prepared.body is not None else b""
    if isinstance(body, str):
        body = body.encode('utf-8')
    return len(request_line.encode('utf-8')) + len(headers_str.encode('utf-8')) + len(body)

def parse_www_authenticate(header):
    """
    Parst den WWW-Authenticate-Header und gibt ein Dictionary mit den Parametern zurück.
    Beispiel-Header:
    Bearer realm="https://ghcr.io/token",service="ghcr.io",scope="repository:chrhermes/fastapi-test:pull"
    """
    auth_params = {}
    pattern = r'(\w+)="([^"]+)"'
    matches = re.findall(pattern, header)
    for key, value in matches:
        auth_params[key] = value
    return auth_params

def get_auth_token(auth_params, username, pat):
    """
    Holt einen Bearer-Token anhand der im WWW-Authenticate-Header gelieferten Parameter.
    Dabei werden sowohl gesendete als auch empfangene Bytes erfasst.
    """
    token_url = auth_params.get("realm")
    if not token_url:
        print("Kein realm im WWW-Authenticate Header gefunden.")
        sys.exit(1)
    service = auth_params.get("service")
    scope = auth_params.get("scope")
    params = {"service": service}
    if scope:
        params["scope"] = scope

    # Request vorbereiten, um gesendete Daten zu messen
    req = requests.Request("GET", token_url, params=params, auth=(username, pat))
    prepared = req.prepare()
    sent_bytes = measure_prepared_request(prepared)
    record_transfer("Token", sent_bytes)

    response = requests.get(token_url, params=params, auth=(username, pat))
    record_transfer("Token", len(response.content))

    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get("token")
        if token:
            return token
        else:
            print("Kein Token in der Antwort gefunden.")
            sys.exit(1)
    else:
        print(f"Fehler beim Abrufen des Tokens: {response.status_code}")
        sys.exit(1)

def get_request_with_auth(url, headers, username, pat, label):
    """
    Führt einen GET-Request aus und misst dabei die gesendeten und empfangenen Daten.
    Falls ein 401-Fehler (Unauthorized) zurückkommt, wird versucht, mit Bearer-Token erneut zuzugreifen.
    """
    # Ersten Request vorbereiten (Basic Auth)
    req = requests.Request("GET", url, headers=headers, auth=(username, pat))
    prepared = req.prepare()
    sent_bytes = measure_prepared_request(prepared)
    record_transfer(label, sent_bytes)
    
    response = requests.get(url, auth=(username, pat), headers=headers)
    record_transfer(label, len(response.content))
    
    if response.status_code == 200:
        return response
    elif response.status_code == 401:
        www_authenticate = response.headers.get("WWW-Authenticate")
        if www_authenticate:
            auth_params = parse_www_authenticate(www_authenticate)
            token = get_auth_token(auth_params, username, pat)
            headers["Authorization"] = f"Bearer {token}"
            # Request mit Token vorbereiten
            req2 = requests.Request("GET", url, headers=headers)
            prepared2 = req2.prepare()
            sent_bytes2 = measure_prepared_request(prepared2)
            record_transfer(label + " mit Token", sent_bytes2)
            
            response2 = requests.get(url, headers=headers)
            record_transfer(label + " mit Token", len(response2.content))
            return response2
        else:
            return response
    else:
        return response

def format_bytes(size):
    """Formatiert die Byte-Größe in ein human readable Format."""
    for unit in ['B', 'kB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def main():
    # Lade Umgebungsvariablen aus der .env-Datei
    load_dotenv()
    USERNAME = os.getenv("USERNAME")
    PAT = os.getenv("PAT")
    REGISTRY = os.getenv("REGISTRY")
    REPO = os.getenv("REPO")

    if not USERNAME or not PAT or not REGISTRY or not REPO:
        print("Fehlende Umgebungsvariablen in der .env-Datei.")
        sys.exit(1)

    # Docker verlangt, dass Username und Repository in Kleinbuchstaben vorliegen
    username_lower = USERNAME.lower()
    repo_lower = REPO.lower()

    if len(sys.argv) < 2:
        print("Usage: python load_label.py <tag>")
        sys.exit(1)
    tag = sys.argv[1]

    # Erstelle den Ausgabeordner ./out, falls nicht vorhanden
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    # Schritt 1: Manifest (Index) abrufen
    manifest_url = f"https://{REGISTRY}/v2/{username_lower}/{repo_lower}/manifests/{tag}"
    headers = {
        "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json"
    }
    response = get_request_with_auth(manifest_url, headers.copy(), USERNAME, PAT, "Manifest (Index)")
    if response.status_code != 200:
        print(f"Fehler beim Laden des Manifests: {response.status_code}")
        print(response.text)
        sys.exit(1)
    manifest_index = response.json()

    # Falls ein Manifest-Index vorliegt, wähle einen passenden Eintrag (z. B. für linux)
    if "manifests" in manifest_index:
        chosen_manifest_digest = None
        for m in manifest_index["manifests"]:
            if m.get("platform", {}).get("os") == "linux":
                chosen_manifest_digest = m["digest"]
                break
        if not chosen_manifest_digest:
            chosen_manifest_digest = manifest_index["manifests"][0]["digest"]
        manifest_url = f"https://{REGISTRY}/v2/{username_lower}/{repo_lower}/manifests/{chosen_manifest_digest}"
        headers = {
            "Accept": "application/vnd.oci.image.manifest.v1+json, application/vnd.docker.distribution.manifest.v2+json"
        }
        response = get_request_with_auth(manifest_url, headers.copy(), USERNAME, PAT, "Manifest (Digest)")
        if response.status_code != 200:
            print(f"Fehler beim Laden des Image-Manifests: {response.status_code}")
            print(response.text)
            sys.exit(1)
        image_manifest = response.json()
    else:
        image_manifest = manifest_index

    # Manifest als Datei speichern im Ordner ./out/
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(image_manifest, f, indent=4)
    print(f"Manifest erfolgreich als {manifest_path} gespeichert.")

    # Schritt 2: Aus dem Manifest den Config-Digest auslesen
    if "config" not in image_manifest:
        print("Kein Config-Objekt im Manifest gefunden.")
        sys.exit(1)
    config_digest = image_manifest["config"]["digest"]

    # Schritt 3: Config-Blob abrufen
    config_url = f"https://{REGISTRY}/v2/{username_lower}/{repo_lower}/blobs/{config_digest}"
    headers = {
        "Accept": "application/vnd.oci.image.config.v1+json, application/vnd.docker.container.image.v1+json"
    }
    response = get_request_with_auth(config_url, headers.copy(), USERNAME, PAT, "Config Blob")
    if response.status_code != 200:
        print(f"Fehler beim Laden des Config-Blobs: {response.status_code}")
        print(response.text)
        sys.exit(1)
    config_blob = response.json()

    # Config-Blob als Datei speichern im Ordner ./out/
    config_blob_path = os.path.join(output_dir, "config_blob.json")
    with open(config_blob_path, "w") as f:
        json.dump(config_blob, f, indent=4)
    print(f"Config-Blob erfolgreich als {config_blob_path} gespeichert.")

    # Schritt 4: Labels aus dem Config-Blob auslesen
    labels = config_blob.get("config", {}).get("Labels", {})
    if not labels:
        print("Keine Labels im Config-Blob gefunden.")
    else:
        print("Gefundene Labels:")
        for key, value in labels.items():
            print(f"{key}: {value}")

    # Gesamtsumme der übertragenen Bytes (gesendet + empfangen)
    total_transferred = sum(transfer_summary.values())
    print(f"\nGesamt übertragen: {format_bytes(total_transferred)}")

if __name__ == "__main__":
    main()
