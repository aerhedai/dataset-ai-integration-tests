import requests
import time

time.sleep(5)  # Wait for APIs to start

# Step 1: Upload dataset
with open('integration_tests/sample_dataset.csv', 'rb') as f:
    files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
    upload_res = requests.post("http://localhost:8001/upload", files=files)

print("Uploader Response:", upload_res.status_code, upload_res.json())

dataset_id = upload_res.json().get("file_id")
if not dataset_id:
    raise Exception("Uploader did not return file_id")

# Step 2: Profile dataset
profile_res = requests.get("http://localhost:8002/profile", params={"dataset_id": dataset_id})

print("Profiler Response:", profile_res.status_code)
print("Profile Output:", profile_res.json())

if profile_res.status_code != 200:
    raise Exception("Profiler API failed")

# Step 3: Clean dataset
clean_res = requests.post("http://localhost:8003/clean", json={"dataset_id": dataset_id})

print("Cleaner Response:", clean_res.status_code)
print("Clean Output:", clean_res.json())

if clean_res.status_code != 200:
    raise Exception("Cleaner API failed")
