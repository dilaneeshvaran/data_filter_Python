import argparse
from data_loader import load_csv, load_json
from data_saver import save_csv, save_json
from data_filter import filter_data
from data_sorter import sort_data

def main():
    parser = argparse.ArgumentParser(description="Data Converter/Filter")
    parser.add_argument('operation', choices=['load', 'save', 'filter', 'sort'], help="Operation to perform")
    parser.add_argument('--input', help="Input file path")
    parser.add_argument('--output', help="Output file path")
    parser.add_argument('--format', choices=['csv', 'json'], help="File format")
    parser.add_argument('--criteria', nargs='+', help="Filter criteria in key=value format")
    parser.add_argument('--sort_key', help="Key to sort data by")

    args = parser.parse_args()

    data = None

    if args.operation == 'load':
        if args.format == 'csv':
            data = load_csv(args.input)
        elif args.format == 'json':
            data = load_json(args.input)
        print(data)

    elif args.operation == 'save':
        if args.format == 'csv':
            save_csv(data, args.output)
        elif args.format == 'json':
            save_json(data, args.output)

    elif args.operation == 'filter':
        criteria = {c.split('=')[0]: c.split('=')[1] for c in args.criteria}
        data = filter_data(data, criteria)
        print(data)

    elif args.operation == 'sort':
        data = sort_data(data, args.sort_key)
        print(data)

if __name__ == '__main__':
    main()
