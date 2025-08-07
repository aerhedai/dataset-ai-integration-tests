import requests
import time

time.sleep(5)

with open('integration_tests/sample_dataset.csv', 'rb') as f:
    files = {"file": ("sample_dataset.csv", f, "application/octet-stream")}
    upload_res = requests.post("http://localhost:8001/upload", files=files)

print("Uploader Response:", upload_res.status_code, upload_res.json())

dataset_id = upload_res.json().get("file_id")
if not dataset_id:
    raise Exception("Uploader did not return file_id")

profile_res = requests.get("http://localhost:8002/profile", params={"dataset_id": dataset_id})

print("Profiler Response:", profile_res.status_code)
print("Profile Output:", profile_res.json())
