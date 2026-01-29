# ⚔️ MMA Fight Predictor

**A lightweight Flask-based project that predicts the likely winner between two MMA fighters using a trained Random Forest model, and provides a simple frontend UI.**

---

## 🚀 Project Overview

This repository contains a small end-to-end pipeline for predicting MMA fight outcomes using fighter-level statistics. The backend exposes a REST API (Flask) that loads a trained model (`saved_models/RandomForestClassifierModel.joblib`) and serves a minimal static frontend (`frontend/`).

## ✨ Features

- Predict winner between two fighters via a REST endpoint. ✅
- Simple autocomplete UI for selecting fighters. ✅
- Uses a saved Random Forest model for inference. ✅
- Local CSV data store for fighter stats and preprocessing scripts. ✅

## 📁 Repository Structure (high level)

- `backend/` — Flask app, API routes, data helpers, and requirements
  - `backend/main.py` — App entry point that serves frontend static files and starts Flask
  - `backend/app/routes.py` — API routes (`/api/fighters`, `/api/health`, `/api/predict`)
  - `backend/data/` — CSVs and `get_data.py` helper
  - `backend/requirements.txt` — Python dependencies
- `frontend/` — Static frontend (`index.html`, `app.js`, `style.css`) that calls the backend API
- `saved_models/` — Trained model (`RandomForestClassifierModel.joblib`)
- `data/` and `data_processor/` — Raw and processor scripts used to build `processed.csv`

---

## 🛠️ Setup (macOS / *nix)

1. Clone the repo:

   ```bash
   git clone <repo-url>
   cd mma-fight-predictor
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install backend requirements:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. Make sure data is available: `backend/data/processed.csv` is expected. If missing, use the scripts in `data_processor/` and the notebooks to regenerate it from `data/original.csv`.

---

## ▶️ Running the app

Start the backend (it serves the frontend too):

```bash
python backend/main.py
```

- App listens on `http://0.0.0.0:8000` by default.
- Visit `http://127.0.0.1:8000/` to use the web UI.

## 🔌 API Endpoints

- `GET /api/fighters` — returns a JSON array of fighter names for autocomplete.
- `GET /api/health` — simple health check (`{"status":"ok"}`).
- `POST /api/predict?fighter1=<name>&fighter2=<name>` — returns prediction JSON. Example (curl):

```bash
curl -X POST "http://127.0.0.1:8000/api/predict?fighter1=Conor%20McGregor&fighter2=Khabib%20Nurmagaomedov"
```

Response includes `fighter1_info`, `fighter2_info`, and `prediction` with `winner` and `confidence`.

---

## 🧠 Model & Data

- Model: `saved_models/RandomForestClassifierModel.joblib` (used in `backend/app/routes.py`).
- Data: CSVs live in `backend/data/` and the top-level `data/` directory. Processor scripts are in `data_processor/` and `backend/data/` includes helpers like `get_data.py`.
- To retrain: follow notebooks in the `models/` and top-level `notebooks/` directories and export a new joblib file into `saved_models/`.

---

## 🧩 Development Notes

- Frontend behavior: `frontend/app.js` hits the API at `http://127.0.0.1:8000/api` and provides autocomplete + prediction UI.
- Add features by editing `backend/app/routes.py` (API) and `frontend/app.js` (UI).
- No tests configured — consider adding unit tests for route logic and model input validation.

> **Note:** If you change CSV filenames or locations, update `backend/app/config.py` (constants for `ORIGINAL_CSV` / `PROCESSED_CSV`).

---

## 🙋 Contributing

Contributions are welcome. Please open issues or PRs for bug fixes, improvements, or model updates.

---

## ⚖️ License

No license specified. Add a `LICENSE` file if you intend to make this project open source.

---

## 📬 Contact

For questions or help, open an issue in this repository.

---

*Generated README — concise reference for contributors & users.*
