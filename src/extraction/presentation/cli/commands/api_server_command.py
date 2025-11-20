import subprocess

def start(host: str = "0.0.0.0", port: int = 8000, reload=True):
    
    print(f"Starting API server on http://{host}:{port}")

    app_path = "geonames.presentation.api.main:app"

    process = subprocess.Popen([
        "uvicorn",
        app_path,
        "--host", host,
        "--port", str(port),
    ])
    return process
