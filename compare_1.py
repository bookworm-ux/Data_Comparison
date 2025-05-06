import json
from deepdiff import DeepDiff

# Example JSON objects

json1 = {
    "total_gross": 124.21,
    "total_net": 116.08,
    "business_name": "Apimeister Consulting GmbH",
    "items": [
        {
            "name": "City Tax",
            "price": 3.0
        },
        {
            "name": "VAT 7%",
            "price": 0.21
        },
        {
            "name": "Mastercard",
            "price": 0.0
        },
        {
            "name": "Accommodation",
            "price": 121.0
        }
    ]
}


json2 = {
    "total_gross": 124.21,
    "total_net": 116.08,
    "business_name": "Premier Inn Hamburg City Zentrum",
    "items": [
        {
            "name": "City Tax",
            "price": 3.0
        },
        {
            "name": "Accommodation",
            "price": 121.0
        }
    ]
}



# Compare using DeepDiff
diff = DeepDiff(json1, json2, ignore_order=True)
print("Differences:\n", json.dumps(diff, indent=2))
