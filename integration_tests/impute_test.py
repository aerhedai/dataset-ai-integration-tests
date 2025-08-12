import requests
import json

sample_data = {
    "rows": [
        {"age": None, "income": 50000},
        {"age": 30, "income": None},
        {"age": 25, "income": 45000}
    ]
}

response = requests.post("http://localhost:8004/impute", json=sample_data)
print(response.status_code)
print(response.json())
