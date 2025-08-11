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
        "      - ./data:/app/data",
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
    "    services:"
]

for api in apis:
    workflow_lines.append(f"      {api['name']}:")
    workflow_lines.append(f"        image: {api['name']}:latest")
    workflow_lines.append(f"        ports:")
    workflow_lines.append(f"          - {api['port']}:{api['internal_port']}")

workflow_lines.extend([
    "    steps:",
    "      - uses: actions/checkout@v2",
    "      - name: Set up Python",
    "        uses: actions/setup-python@v2",
    "        with:",
    "          python-version: '3.x'",
    "      - name: Install dependencies",
    "        run: pip install requests",
    "      - name: Wait for APIs to start",
    "        run: sleep 10",
    "      - name: Run integration tests",
    "        run: python integration_tests/test_pipeline.py"
])

with open(os.path.join(workflow_dir, "integration-test.yml"), "w") as f:
    f.write("\n".join(workflow_lines) + "\n")

print("Generated .github/workflows/integration-test.yml")
