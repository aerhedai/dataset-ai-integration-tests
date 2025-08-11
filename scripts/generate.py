import json
import os

# Load API definitions
with open("apis.json") as f:
    apis = json.load(f)

# --- Generate .gitmodules ---
with open(".gitmodules", "w") as f:
    for api in apis:
        f.write(f'[submodule "{api["name"]}"]\n')
        f.write(f'\tpath = {api["path"]}\n')
        f.write(f'\turl = {api["repo"]}\n\n')

print("Generated .gitmodules")

# --- Generate docker-compose.yml ---
compose_lines = [
    "version: '3.9'",
    "services:"
]

for idx, api in enumerate(apis):
    service_lines = [
        f"  {api['name']}:",
        "    build:",
        f"      context: ./{api['path']}",
        "    ports:",
        f"      - \"{api['port']}:{api['internal_port']}\"",
        "    volumes:",
        "      - ./integration_tests:/app/integration_tests",
        "      - ./uploaded_files:/app/uploaded_files",
        "    networks:",
        "      - ai-net",
    ]
    if idx > 0:
        depends_on_service = apis[idx - 1]["name"]
        service_lines.append("    depends_on:")
        service_lines.append(f"      - {depends_on_service}")

    compose_lines.extend(service_lines)

compose_lines.append(
    "networks:\n"
    "  ai-net:\n"
    "    driver: bridge\n"
)

with open("docker-compose.yml", "w") as f:
    f.write("\n".join(compose_lines) + "\n")

print("Generated docker-compose.yml")

# --- Generate GitHub Actions workflow ---
workflow_dir = ".github/workflows"
os.makedirs(workflow_dir, exist_ok=True)

workflow_lines = [
    "name: Integration Tests",
    "on: [push, pull_request]",
    "jobs:",
    "  test_pipeline:",
    "    runs-on: ubuntu-latest",
    "    steps:",
    "    - name: Checkout repository with submodules",
    "      uses: actions/checkout@v3",
    "      with:",
    "        submodules: true",
    "    - name: Initialize and update submodules",
    "      run: git submodule update --init --recursive",
    "    - name: Build and start APIs with Docker Compose",
    "      run: docker compose up -d --build",
    "    - name: Wait for APIs to start",
    "      run: sleep 15",
    "    - name: Set up Python",
    "      uses: actions/setup-python@v4",
    "      with:",
    "        python-version: '3.x'",
    "    - name: Install dependencies",
    "      run: pip install requests",
    "    - name: Run integration tests",
    "      run: python integration_tests/test_pipeline.py",
    "    - name: Tear down Docker Compose",
    "      if: always()",
    "      run: docker compose down"
]

with open(os.path.join(workflow_dir, "integration-test.yml"), "w") as f:
    f.write("\n".join(workflow_lines) + "\n")

print("Generated .github/workflows/integration-test.yml")
