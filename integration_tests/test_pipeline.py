import requests
import time
import json
import os
import sys

APIS_JSON_PATH = os.path.join(".", "apis.json")
SAMPLE_DATA_PATH = os.path.join("integration_tests", "sample_dataset.csv")

def load_apis():
    with open(APIS_JSON_PATH, "r") as f:
        return json.load(f)

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
    try:
        url = f"http://localhost:{api['port']}{api['test_endpoint']['path']}"
        method = api['test_endpoint']['method'].lower()

        if method == "get":
            params = {}
            if "query_param" in api['test_endpoint']:
                params[api['test_endpoint']['query_param']] = dataset_id
            resp = requests.get(url, params=params)
        elif method == "post":
            if api['test_endpoint'].get("upload_file", False):
                # This case is covered by uploader; just in case here
                with open(SAMPLE_DATA_PATH, "rb") as f:
                    files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
                    resp = requests.post(url, files=files)
            else:
                json_key = api['test_endpoint'].get("json_key", "dataset_id")
                resp = requests.post(url, json={json_key: dataset_id})
        else:
            print(f"Unsupported HTTP method for {api['name']}")
            return dataset_id  # Continue pipeline with same id

        resp.raise_for_status()
        print(f"{api['name']} Response:", resp.status_code)
        print(f"{api['name']} Output:", resp.json())

        # Update dataset_id if new one returned, else pass current forward
        return resp.json().get("cleaned_id") or resp.json().get("file_id") or dataset_id

    except Exception as e:
        print(f"{api['name']} test failed: {e}")
        if api['test_endpoint'].get("required", False):
            print(f"{api['name']} is required. Aborting pipeline test.")
            sys.exit(1)
        return dataset_id  # Continue with current id despite failure

def main():
    print("Waiting for containers to be ready...")
    time.sleep(5)

    apis = load_apis()

    dataset_id = None
    for i, api in enumerate(apis):
        # Run uploader test first (upload_file expected)
        if i == 0 and api['test_endpoint'].get("upload_file", False):
            dataset_id = test_upload(api)
        else:
            dataset_id = test_api(api, dataset_id)

if __name__ == "__main__":
    main()
