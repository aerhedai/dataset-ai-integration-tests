import requests
import time
import json
import os
import sys
import csv

APIS_JSON_PATH = os.path.join(".", "apis.json")
SAMPLE_DATA_PATH = os.path.join("integration_tests", "sample_dataset.csv")

def load_apis():
    with open(APIS_JSON_PATH, "r") as f:
        return json.load(f)

def load_sample_rows():
    with open(SAMPLE_DATA_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def test_upload(api):
    print(f"\n--- Testing {api['name']} (upload) ---")
    with open(SAMPLE_DATA_PATH, "rb") as f:
        files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
        try:
            resp = requests.post(f"http://localhost:{api['port']}{api['test_endpoint']['path']}", files=files)
            resp.raise_for_status()
            print(f"{api['name']} Response:", resp.status_code, resp.json())
            file_id = resp.json().get("file_id")
            if not file_id:
                raise Exception(f"{api['name']} did not return file_id")
            return file_id
        except Exception as e:
            print(f"{api['name']} test failed: {e}")
            if api['test_endpoint'].get("required", False):
                print("Uploader API is required. Aborting pipeline test.")
                sys.exit(1)
            return None

def test_api(api, dataset_id):
    print(f"\n--- Testing {api['name']} ---")
    if not dataset_id:
        print(f"Skipping {api['name']} test: no dataset_id available")
        return None
    
    # Support single or multiple endpoints per API
    endpoints = api.get("test_endpoints") or [api.get("test_endpoint")]
    if not endpoints or endpoints == [None]:
        print(f"No test endpoints defined for {api['name']}. Skipping.")
        return dataset_id

    for endpoint in endpoints:
        path = endpoint["path"]
        method = endpoint["method"].lower()
        url = f"http://localhost:{api['port']}{path}"

        try:
            if method == "get":
                params = {}
                if "query_param" in endpoint:
                    params[endpoint["query_param"]] = dataset_id
                resp = requests.get(url, params=params)

            elif method == "post":
                # Prepare payload based on API and endpoint
                if endpoint.get("upload_file", False):
                    # Upload endpoint - already covered, but just in case
                    with open(SAMPLE_DATA_PATH, "rb") as f:
                        files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
                        resp = requests.post(url, files=files)
                else:
                    # Special handling for data-preparation-api endpoints
                    if api["name"] == "data-preparation-api":
                        rows = load_sample_rows()
                        if path == "/leakage":
                            payload = {
                                "rows": rows,
                                "target_column": "target"  # change this to your actual target column name
                            }
                        elif path in ["/impute", "/features"]:
                            payload = {
                                "rows": rows
                            }
                        else:
                            # Default payload for unknown endpoints
                            payload = {endpoint.get("json_key", "dataset_id"): dataset_id}
                        resp = requests.post(url, json=payload)
                    else:
                        # Default for other APIs
                        json_key = endpoint.get("json_key", "dataset_id")
                        resp = requests.post(url, json={json_key: dataset_id})

            else:
                print(f"Unsupported HTTP method for {api['name']} at {path}")
                continue

            resp.raise_for_status()
            print(f"{api['name']} ({path}) Response:", resp.status_code)
            print(f"{api['name']} ({path}) Output:", resp.json())

            # Update dataset_id if new one returned, else keep same
            dataset_id = resp.json().get("cleaned_id") or resp.json().get("file_id") or dataset_id

        except Exception as e:
            print(f"{api['name']} ({path}) test failed: {e}")
            if endpoint.get("required", False):
                print(f"{api['name']} is required. Aborting pipeline test.")
                sys.exit(1)
            # else continue with next endpoint or API

    return dataset_id

def main():
    print("Waiting for containers to be ready...")
    time.sleep(5)

    apis = load_apis()

    dataset_id = None
    for i, api in enumerate(apis):
        # If uploader API with upload_file endpoint, run upload test
        if i == 0 and api.get("test_endpoint", {}).get("upload_file", False):
            dataset_id = test_upload(api)
        else:
            dataset_id = test_api(api, dataset_id)

if __name__ == "__main__":
    main()
