import argparse
import os
import json
from data_loader import load_csv, load_json
from data_saver import save_csv, save_json
from data_filter import filter_data
from data_sorter import sort_data

data = None

def main():
    global data
    parser = argparse.ArgumentParser(description="Data Converter/Filter")
    parser.add_argument('operation', choices=['load', 'save', 'filter', 'sort'], help="Operation to perform")
    parser.add_argument('--input', help="Input file path")
    parser.add_argument('--output', help="Output file path")
    parser.add_argument('--format', choices=['csv', 'json'], help="File format")
    parser.add_argument('--criteria', nargs='+', help="Filter criteria in key=operator=value format (e.g., 'Spotify Streams>100000')")
    parser.add_argument('--sort_key', help="Key to sort data by (e.g., 'Spotify Streams, YouTube Likes, TikTok Likes, TikTok Views')")

    args = parser.parse_args()

    if args.operation == 'load':
        if args.format == 'csv':
            data = load_csv(args.input)
        elif args.format == 'json':
            data = load_json(args.input)
        with open('temp_data.json', 'w') as f:
            json.dump(data, f)
        print("Data Loaded")

    elif args.operation == 'save':
        if data is None and os.path.exists('temp_data.json'):
            with open('temp_data.json', 'r') as f:
                data = json.load(f)
        if data is None:
            print("No data to save. Please load the data first.")
            return
        if args.format == 'csv':
            save_csv(data, args.output)
        elif args.format == 'json':
            save_json(data, args.output)
        print("Data Saved")

    elif args.operation == 'filter':
        if data is None and os.path.exists('temp_data.json'):
            with open('temp_data.json', 'r') as f:
                data = json.load(f)
        if data is None:
            print("No data to filter. Please load the data first.")
            return
        criteria = []
        for c in args.criteria:
            if '>' in c:
                key, value = c.split('>', 1)
                criteria.append((key.strip(), '>', value.strip()))
            elif '<' in c:
                key, value = c.split('<', 1)
                criteria.append((key.strip(), '<', value.strip()))
            elif '=' in c:
                key, value = c.split('=', 1)
                criteria.append((key.strip(), '=', value.strip()))
            else:
                print(f"Invalid criteria format: {c}. Expected format: key=operator=value")
        data = filter_data(data, criteria)
        with open('temp_data.json', 'w') as f:
            json.dump(data, f)
        print("Data Filtered")

    elif args.operation == 'sort':
        if data is None and os.path.exists('temp_data.json'):
            with open('temp_data.json', 'r') as f:
                data = json.load(f)
        if data is None:
            print("No data to sort. Please load the data first.")
            return
        data = sort_data(data, args.sort_key)
        with open('temp_data.json', 'w') as f:
            json.dump(data, f)
        print("Data Sorted")

if __name__ == '__main__':
    main()
