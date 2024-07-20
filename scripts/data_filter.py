import json
import statistics

def filter_data(data, criteria, global_stats=None):
    def matches_criteria(item):
        for field, op, value in criteria:
            if field == 'prix_x_quantite':
                try:
                    total_value = float(item.get('price', 0)) * float(item.get('quantity', 0))
                    if not eval(f"total_value {op} {value}"):
                        return False
                except ValueError:
                    return False
                continue

            item_value = item.get(field)
            if item_value is None:
                return False

            # Handle string operations
            if isinstance(item_value, str) and not (item_value.startswith("[") and item_value.endswith("]")):
                if op == 'contient' and value not in item_value:
                    return False
                if op == 'commence' and not item_value.startswith(value):
                    return False
                if op == 'finit' and not item_value.endswith(value):
                    return False
                # Lexicographic comparisons
                if op == '<' and item_value >= value:
                    return False
                if op == '>' and item_value <= value:
                    return False

            # Handle list operations
            elif isinstance(item_value, str) and item_value.startswith("[") and item_value.endswith("]"):
                try:
                    item_list = [float(i) for i in item_value.split(',')]
                except ValueError:
                    return False
                if op == 'min' and min(item_list) <= float(value):
                    return False
                if op == 'max' and max(item_list) >= float(value):
                    return False
                if op == 'moyenne' and statistics.mean(item_list) <= float(value):
                    return False
                if op == 'length' and len(item_list) != int(value):
                    return False
                if op == 'length>' and len(item_list) <= int(value):
                    return False
                if op == 'length<' and len(item_list) >= int(value):
                    return False

            # Handle numeric comparisons
            elif isinstance(item_value, (int, float, bool)):
                try:
                    item_value = float(item_value)
                    value = float(value)
                except ValueError:
                    return False

                if op == '=' and item_value != value:
                    return False
                elif op == '>' and item_value <= value:
                    return False
                elif op == '<' and item_value >= value:
                    return False

            # Handle field-to-field comparisons
            if op in ['avant', 'apres', 'egal', 'plus_haut', 'plus_bas']:
                other_field_value = item.get(value.strip())
                if other_field_value is None:
                    return False
                try:
                    if op in ['plus_haut', 'plus_bas']:
                        item_value = float(item_value)
                        other_field_value = float(other_field_value)
                    if op == 'avant' and not item_value < other_field_value:
                        return False
                    if op == 'apres' and not item_value > other_field_value:
                        return False
                    if op == 'egal' and not item_value == other_field_value:
                        return False
                    if op == 'plus_haut' and not item_value > other_field_value:
                        return False
                    if op == 'plus_bas' and not item_value < other_field_value:
                        return False
                except ValueError:
                    return False

            # Handle global statistics comparisons
            if global_stats:
                if op == 'plus_vieux_que_moyenne' and not item_value > global_stats.get('age', 0):
                    return False
                if op == 'moins_cher_que_75' and not item_value < global_stats.get('prix_75', float('inf')):
                    return False

        return True

    return [item for item in data if matches_criteria(item)]

def calculate_global_stats(data):
    stats = {}
    ages = [float(item.get('age', 0)) for item in data if 'age' in item]
    prix = [float(item.get('price', 0)) for item in data if 'price' in item]

    if ages:
        stats['age'] = statistics.mean(ages)
    if prix:
        stats['prix_75'] = sorted(prix)[int(0.75 * len(prix))]

    return stats