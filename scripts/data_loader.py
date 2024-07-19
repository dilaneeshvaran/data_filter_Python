import csv
import json
import yaml
import xml.etree.ElementTree as ET

def load_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for child in root:
        item = {}
        for subchild in child:
            item[subchild.tag] = subchild.text
        data.append(item)
    return data

def display_sample(data):
    for item in data[:5]:
        print(json.dumps(item, indent=4))
