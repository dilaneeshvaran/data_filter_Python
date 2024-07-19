import csv
import json
import yaml
import xml.etree.ElementTree as ET

def save_csv(data, file_path):
    keys = data[0].keys()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def save_json(data, file_path):
    with open(file_path, mode='w') as file:
        json.dump(data, file, indent=4)

def save_yaml(data, file_path):
    with open(file_path, mode='w') as file:
        yaml.dump(data, file)

def save_xml(data, file_path):
    root = ET.Element("root")
    for item in data:
        item_elem = ET.SubElement(root, "item")
        for key, value in item.items():
            child = ET.SubElement(item_elem, key)
            child.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(file_path)

