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
  ```bash
  git clone https://github.com/aerhedai/dataset-uploader-api.git
  git clone https://github.com/aerhedai/data-profiler-api.git
  ```

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

## 🔁 How File Sharing Works

- The **uploader saves** files to: `/app/uploaded_files/{file_id}.csv`
- The **profiler reads** files from: `/app/uploaded_files/{file_id}.csv`
- Both services mount the same host path (`./uploaded_files`) to ensure access.

---

## 🐞 Troubleshooting

| Issue | Cause | Fix |
|------|-------|-----|
| `415 Unsupported Media Type` | Wrong file format in upload | Ensure you're sending `multipart/form-data` with correct MIME |
| `405 Method Not Allowed` | Wrong HTTP method | Check you’re using `POST` not `GET` |
| `500 Internal Server Error` from profiler | File not found | Ensure shared volume is working and file path matches |
| `FileNotFoundError` on `sample_dataset.csv` | Wrong relative path | Ensure you run test from repo root |

---

## 🧪 `test_pipeline.py` Summary

```python
with open('integration_tests/sample_dataset.csv', 'rb') as f:
    files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
    upload_res = requests.post("http://localhost:8001/upload", files=files)

file_id = upload_res.json()["file_id"]
file_path = f"/app/uploaded_files/{file_id}.csv"

profile_res = requests.post("http://localhost:8002/profile", params={"dataset_id": file_id})
```

Note: Adjust if your profiler uses JSON body instead of query params.

---

## 🧹 Cleanup

```bash
docker-compose down --volumes
```

---

## 🔧 docker-compose.yml Overview

```yaml
version: '3.9'
services:
  uploader-api:
    build: ./dataset-uploader-api
    ports:
      - "8001:8080"
    volumes:
      - ./integration_tests:/app/integration_tests
      - ./uploaded_files:/app/uploaded_files
    networks:
      - ai-net

  profiler-api:
    build: ./data-profiler-api
    ports:
      - "8002:8080"
    depends_on:
      - uploader-api
    volumes:
      - ./integration_tests:/app/integration_tests
      - ./uploaded_files:/app/uploaded_files
    networks:
      - ai-net

networks:
  ai-net:
    driver: bridge
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
