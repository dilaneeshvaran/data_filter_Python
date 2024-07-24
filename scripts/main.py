import argparse
import os
import json
from data_loader import load_csv, load_json, load_yaml, load_xml, display_sample
from data_saver import save_csv, save_json, save_yaml, save_xml
from data_filter import filter_data, calculate_global_stats
from data_sorter import sort_data
from data_stat import calculate_statistics
from interface import run_interface

data = None
original_data = None
historique_filtrages = []
redo_stack = []



def main():
    global data, original_data
    parser = argparse.ArgumentParser(description="Data Converter/Filter")
    parser.add_argument('operation', choices=['load', 'save', 'filter', 'sort', 'stats', 'interface', 'undo', 'redo', 'afficher_historique'], help="Operation to perform")
    parser.add_argument('--input', help="Input file path")
    parser.add_argument('--output', help="Output file path")
    parser.add_argument('--format', choices=['csv', 'json', 'yaml', 'xml'], help="File format")
    parser.add_argument('--criteria', nargs='+', help="Filter criteria in key=operator=value format (e.g., 'apprentice=true')")
    parser.add_argument('--sort_key', help="Key to sort data by (e.g., 'Spotify Streams, YouTube Likes, TikTok Likes, TikTok Views')")

    args = parser.parse_args()

    if args.operation == 'interface':
        run_interface()
        return

    if args.operation == 'load':
        if args.format == 'csv':
            data = load_csv(args.input)
        elif args.format == 'json':
            data = load_json(args.input)
        elif args.format == 'yaml':
            data = load_yaml(args.input)
        elif args.format == 'xml':
            data = load_xml(args.input)
        original_data = data.copy()  # Save the original data
        with open('temp_data.json', 'w') as f:
            json.dump(data, f)
        print("Data Loaded")
        display_sample(data)

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
        elif args.format == 'yaml':
            save_yaml(data, args.output)
        elif args.format == 'xml':
            save_xml(data, args.output)
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
            elif 'contient' in c:
                key, value = c.split('contient', 1)
                criteria.append((key.strip(), 'contient', value.strip().strip("'").strip()))
            elif 'commence' in c:
                key, value = c.split('commence', 1)
                criteria.append((key.strip(), 'commence', value.strip().strip("'").strip()))
            elif 'finit' in c:
                key, value = c.split('finit', 1)
                criteria.append((key.strip(), 'finit', value.strip().strip("'").strip()))
            elif 'min' in c:
                key, value = c.split('min', 1)
                criteria.append((key.strip(), 'min', value.strip()))
            elif 'max' in c:
                key, value = c.split('max', 1)
                criteria.append((key.strip(), 'max', value.strip()))
            elif 'moyenne' in c:
                key, value = c.split('moyenne', 1)
                criteria.append((key.strip(), 'moyenne', value.strip()))
            elif 'length' in c:
                key, value = c.split('length', 1)
                if value.startswith('>'):
                    criteria.append((key.strip(), 'length>', value[1:].strip()))
                elif value.startswith('<'):
                    criteria.append((key.strip(), 'length<', value[1:].strip()))
                else:
                    criteria.append((key.strip(), 'length', value.strip()))
            elif 'avant' in c or 'apres' in c or 'egal' in c or  'plus_haut' in c or 'plus_bas' in c:
                key, op = c.split(' ', 1)
                criteria.append((key.strip(), op.strip(), ''))
            elif 'plus_vieux_que_moyenne' in c or 'moins_cher_que_75' in c:
                criteria.append((c.strip(), 'global', ''))
            else:
                print(f"Invalid criteria format: {c}. Expected format: key=operator=value")

                with open('temp_data.json', 'w') as f:
                    json.dump(data, f)
        print("Data Filtered")
        display_sample(data)

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
        display_sample(data)

    elif args.operation == 'stats':
        if data is None and os.path.exists('temp_data.json'):
            with open('temp_data.json', 'r') as f:
                data = json.load(f)
        if data is None:
            print("No data to calculate statistics. Please load the data first.")
            return
        stats = calculate_statistics(data)
        print(json.dumps(stats, indent=4))



if __name__ == '__main__':
    main()
