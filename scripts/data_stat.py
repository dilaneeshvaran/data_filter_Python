import json
import numpy as np
import pandas as pd

def calculate_statistics(data):
    df = pd.DataFrame(data)
    stats = {}

    for column in df.columns:
        values = df[column].dropna()

        if pd.api.types.is_numeric_dtype(values):
            stats[column] = {
                'min': float(values.min()),
                'max': float(values.max()),
                'mean': float(values.mean())
            }
        elif pd.api.types.is_bool_dtype(values):
            true_count = values.sum()
            false_count = len(values) - true_count
            stats[column] = {
                'true_percent': (true_count / len(values)) * 100,
                'false_percent': (false_count / len(values)) * 100
            }
        elif all(isinstance(x, str) and x.startswith('[') and x.endswith(']') for x in values):
            list_values = [json.loads(x) for x in values]
            list_lengths = [len(l) for l in list_values]
            flat_values = [item for sublist in list_values for item in sublist]
            stats[column] = {
                'min_length': int(np.min(list_lengths)),
                'max_length': int(np.max(list_lengths)),
                'mean_length': float(np.mean(list_lengths)),
                'min_value': float(np.min(flat_values)),
                'max_value': float(np.max(flat_values)),
                'mean_value': float(np.mean(flat_values))
            }
        elif all(isinstance(x, str) and ',' in x for x in values):
            list_values = [list(map(float, x.split(','))) for x in values]
            list_lengths = [len(l) for l in list_values]
            flat_values = [item for sublist in list_values for item in sublist]
            stats[column] = {
                'min_length': int(np.min(list_lengths)),
                'max_length': int(np.max(list_lengths)),
                'mean_length': float(np.mean(list_lengths)),
                'min_value': float(np.min(flat_values)),
                'max_value': float(np.max(flat_values)),
                'mean_value': float(np.mean(flat_values))
            }

    return stats


