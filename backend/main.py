from app import create_app
from flask import send_from_directory
import os
from pathlib import Path

app = create_app()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

@app.route('/frontend/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0', 
        port=8000
    )