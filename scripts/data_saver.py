import csv
import json

def save_csv(data, file_path):
    if not data:
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_json(data, file_path):
    with open(file_path, mode='w') as file:
        json.dump(data, file, indent=4)
