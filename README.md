# 🧪 Dataset AI Integration Tests

This repository contains **integration tests** for the [dataset-uploader-api](https://github.com/aerhedai/dataset-uploader-api) and [data-profiler-api](https://github.com/aerhedai/data-profiler-api). It verifies the full data pipeline: uploading a dataset, then profiling it using a second service — all inside Docker containers with a shared volume.

---

## 📁 Project Structure

```
dataset-ai-integration-tests/
│
├── integration_tests/
│   ├── sample_dataset.csv         # Sample CSV used for testing
│   └── test_pipeline.py           # Pipeline test script
│
├── dataset-uploader-api/          # (git submodule or copy of uploader API)
│
├── data-profiler-api/             # (git submodule or copy of profiler API)
│
├── uploaded_files/                # Shared volume for dataset file access
│
└── docker-compose.yml             # Runs both APIs with volume/network setup
```

---

## 🚀 Quick Start

### 1. ✅ Prerequisites

- Python 3.8+
- Docker + Docker Compose installed
- Clone the necessary API repos into this directory:

> Or link them as Git submodules for better modularity.

---

### 2. 📦 Build & Start Services

From the root of this repo:

```bash
docker-compose up --build
```

This will:
- Build and start both `uploader-api` and `profiler-api`.
- Map ports:
  - Uploader: [http://localhost:8001](http://localhost:8001)
  - Profiler: [http://localhost:8002](http://localhost:8002)
  - All other apis in the pipeline...
- Mount a **shared volume** at `./uploaded_files` inside both containers for file handoff.

---

### 3. 🧪 Run the Integration Test

Wait 5–10 seconds for containers to fully boot, then run:

```bash
python integration_tests/test_pipeline.py
```

This test:
1. Uploads `sample_dataset.csv` to the uploader API.
2. Extracts the returned `file_id`.
3. Passes that to the profiler API.
4. Prints both API responses and the final profiling output.

---

## 🔍 Example Output

```bash
Uploader Response: 200 {'file_id': '936d6d0b8df94f7182c14ea508c95373', 'filename': 'sample_dataset.csv'}
Profiler Response: 200
Profile Output: {
  "summary": { ... },
  "column_types": { ... },
  ...
}
```

---

## 🧹 Cleanup

```bash
docker-compose down --volumes
```
---

## 🧠 Authors & Credits

Developed by [@rohanpatel](https://github.com/aerhedai) using modular AI APIs for dataset automation.

---

## 🛠 Future Work

- Add automatic test runners (e.g. `pytest`) and assertions
- Add GitHub Actions for CI on every push
- Add tests for malformed CSVs, empty files, etc.

---
