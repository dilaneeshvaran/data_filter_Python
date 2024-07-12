import csv
import json

def load_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def load_json(file_path):
    with open(file_path, mode='r') as file:
        return json.load(file)
