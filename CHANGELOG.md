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

## [1.1.0] - 2025-08-11

### ✨ Added
- Integrated **data-cleaner-api** into the pipeline testing suite.
- Updated `test_pipeline.py` to:
  - Upload dataset via uploader API.
  - Profile dataset with profiler API.
  - Clean dataset using cleaner API.
  - Print responses and reports at each stage.
- Extended Docker Compose to include cleaner-api service with shared volumes and networking.
- Enhanced pipeline coverage for end-to-end dataset processing.

## [2.0.0] - 2025-08-12

### 🚀 Major Automation Release

- Introduced **generate.py** script to fully automate:
  - `.gitmodules`
  - `docker-compose.yml`
  - GitHub Actions workflow (`.github/workflows/integration-test.yml`)
- API definitions maintained centrally in `apis.json`.
- Eliminated manual updates for submodules, Docker services, and CI pipelines when adding/removing APIs.
- Seamless integration testing pipeline that scales with growing API count.
- Improved developer experience and reduced error-prone manual config changes.

## [2.1.0] - 2025-08-12

### ✨ Added
- Integrated **data-preparation-api** into the dataset AI pipeline testing suite.
- Extended testing framework to support APIs with multiple endpoints (`/impute`, `/features`, `/leakage`).
- Enhanced `test_pipeline.py` to handle multi-endpoint APIs with flexible JSON payloads per endpoint.
- Updated `apis.json` to define multiple test endpoints per API with custom payloads and required flags.
- Validated end-to-end flow including data upload, profiling, cleaning, imputation, feature engineering, and leakage detection.
- Improved error handling and logging in integration tests for better debugging.
- Documented expected input and output formats for data-preparation-api endpoints.
- Established manual and automated verification methods to confirm APIs apply meaningful data transformations.

### 🛠 Fixed
- Resolved key errors in testing script related to handling single vs multiple endpoints.
- Adjusted Docker Compose and submodule generation to accommodate complex multi-function APIs.

### 📁 Updates
- Sample dataset used for pipeline testing includes missing values and diverse feature types to enable meaningful imputation and feature engineering.
- CI/CD workflow updated to build, start, test, and tear down multi-endpoint API containers seamlessly.

---

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