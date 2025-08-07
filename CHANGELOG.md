# 📦 Changelog

## [1.0.0] - 2025-08-07

### 🚀 Initial Release

This is the first official release of the **Dataset AI Integration Tests** project, designed to test the complete pipeline between modular AI APIs.

### ✅ Features

- 🔁 End-to-end integration between:
  - [`dataset-uploader-api`](https://github.com/aerhedai/dataset-uploader-api)
  - [`data-profiler-api`](https://github.com/aerhedai/data-profiler-api)
- 🐍 Python test script (`test_pipeline.py`) to:
  - Upload a sample CSV
  - Receive a `file_id`
  - Pass the ID to the profiler
  - Print out structured profiling output
- 🐳 Docker Compose setup for:
  - Isolated API containers
  - Shared network (`ai-net`)
  - Shared volume (`uploaded_files/`) for file exchange
- 🧪 Sample dataset included for testing

### 📁 Directory Structure

- `integration_tests/`: Contains CSV and test logic
- `docker-compose.yml`: Defines environment for uploader + profiler
- Shared `uploaded_files/` ensures profiler can access uploaded CSVs

---

### 🛠 Setup & Use

1. Build & start services via `docker-compose up --build`
2. Run test: `python integration_tests/test_pipeline.py`

---

### 🧹 Known Limitations

- No formal test assertions yet (just prints output)
- Profiler may fail if `file_id` mapping breaks
- No CI/CD integration — tests must be run manually

---